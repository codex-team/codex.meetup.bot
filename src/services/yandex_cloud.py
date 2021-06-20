import logging

from google.protobuf.json_format import MessageToDict
from yandex.cloud.compute.v1.image_service_pb2 import GetImageLatestByFamilyRequest
from yandex.cloud.compute.v1.image_service_pb2_grpc import ImageServiceStub
from yandex.cloud.compute.v1.instance_pb2 import IPV4, Instance
from yandex.cloud.compute.v1.instance_service_pb2 import (
    CreateInstanceRequest,
    ResourcesSpec,
    AttachedDiskSpec,
    NetworkInterfaceSpec,
    PrimaryAddressSpec,
    OneToOneNatSpec,
    CreateInstanceMetadata,
    DeleteInstanceRequest, DeleteInstanceMetadata,
)
from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub
import os
import yandexcloud
import json
from yandexcloud import SDK

script_dir = os.path.dirname(__file__)
rel_path = "../../key.json"
abs_file_path = os.path.join(script_dir, rel_path)

with open(abs_file_path) as json_file:
    sa_key = json.load(json_file)

sdk: SDK = yandexcloud.SDK(service_account_key=sa_key)
instance_service = sdk.client(InstanceServiceStub)


def create_instance(folder_id, zone, name, subnet_id):
    image_service = sdk.client(ImageServiceStub)
    source_image = image_service.GetLatestByFamily(
        GetImageLatestByFamilyRequest(
            folder_id='standard-images',
            family='ubuntu-2004-lts'
        )
    )
    subnet_id = subnet_id or sdk.helpers.find_subnet_id(folder_id, zone)
    operation = instance_service.Create(CreateInstanceRequest(
        folder_id=folder_id,
        name=name,
        resources_spec=ResourcesSpec(
            memory=1 * 2 ** 30,
            cores=2,
            core_fraction=20,
        ),
        zone_id=zone,
        platform_id='standard-v1',
        boot_disk_spec=AttachedDiskSpec(
            auto_delete=True,
            disk_spec=AttachedDiskSpec.DiskSpec(
                type_id='network-ssd',
                size=10 * 2 ** 30,
                image_id=source_image.id,
            )
        ),
        network_interface_specs=[
            NetworkInterfaceSpec(
                subnet_id=subnet_id,
                primary_v4_address_spec=PrimaryAddressSpec(
                    one_to_one_nat_spec=OneToOneNatSpec(
                        ip_version=IPV4,
                    )
                )
            ),
        ],
    ))
    logging.info('Creating initiated')

    operation_result = sdk.wait_operation_and_get_result(
        operation,
        response_type=Instance,
        meta_type=CreateInstanceMetadata,
    )

    return MessageToDict(operation_result.response)


def delete_instance(instance_id):
    operation = instance_service.Delete(
        DeleteInstanceRequest(instance_id=instance_id))

    operation_result = sdk.wait_operation_and_get_result(
        operation,
        response_type=Instance,
        meta_type=DeleteInstanceMetadata,
    )

    return MessageToDict(operation_result.response)
