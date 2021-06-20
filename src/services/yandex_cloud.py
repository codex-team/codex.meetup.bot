import logging
from yandex.cloud.compute.v1.image_service_pb2 import GetImageLatestByFamilyRequest
from yandex.cloud.compute.v1.image_service_pb2_grpc import ImageServiceStub
from yandex.cloud.compute.v1.instance_pb2 import IPV4, Instance
from yandex.cloud.compute.v1.instance_service_pb2 import (
    CreateInstanceRequest,
    ResourcesSpec,
    AttachedDiskSpec,
    NetworkInterfaceSpec,
    PrimaryAddressSpec,
    OneToOneNatSpec, CreateInstanceMetadata,
)
from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub
import os

script_dir = os.path.dirname(__file__)
rel_path = "../../key.json"
abs_file_path = os.path.join(script_dir, rel_path)

import yandexcloud

import json

with open(abs_file_path) as json_file:
    sa_key = json.load(json_file)

sdk = yandexcloud.SDK(service_account_key=sa_key)


def create_instance(folder_id, zone, name, subnet_id):
    image_service = sdk.client(ImageServiceStub)
    source_image = image_service.GetLatestByFamily(
        GetImageLatestByFamilyRequest(
            folder_id='standard-images',
            family='ubuntu-2004-lts'
        )
    )
    subnet_id = subnet_id or sdk.helpers.find_subnet_id(folder_id, zone)
    instance_service = sdk.client(InstanceServiceStub)
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

    return operation_result.response
