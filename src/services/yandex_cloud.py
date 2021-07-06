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

from src.services.env import YANDEX_CLOUD_FOLDER_ID

script_dir = os.path.dirname(__file__)
rel_path = "../../key.json"
abs_file_path = os.path.join(script_dir, rel_path)

with open(abs_file_path) as json_file:
    sa_key = json.load(json_file)


def create_instance(name):
    sdk: SDK = yandexcloud.SDK(service_account_key=sa_key)
    instance_service = sdk.client(InstanceServiceStub)
    zone = 'ru-central1-a'
    image_service = sdk.client(ImageServiceStub)
    source_image = image_service.GetLatestByFamily(
        GetImageLatestByFamilyRequest(
            folder_id='standard-images',
            family='ubuntu-2004-lts'
        )
    )
    subnet_id = sdk.helpers.find_subnet_id(YANDEX_CLOUD_FOLDER_ID, zone)
    operation = instance_service.Create(CreateInstanceRequest(
        folder_id=YANDEX_CLOUD_FOLDER_ID,
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
        metadata={
            'ssh-keys': 'root:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDDtzMIUkBrEh/JTL2lRPTj2QZnOqQDcRdoLAHknN2Xax8podwaiZuwVYVmLTnTmy2Q8V9i9ibJg6tTefLF+FWi4NkWz1f8uMgpnQadnmq33T81n75aqZwx6jdSdEt98VJNlPK6epdB5PnOJDVNg3nx4pEzYsv0RaFQjC6hWEWbAot8aWj4rO4beYB75fRf2u6pIvoF7P4oXM4EC/SYPwN8DQrvZYLEiKsbeJK/mhG3iryvN9C7tPOs8igQU8Is40Xd3p04bI55/6TqpaTySsgEMup7UbPAue5jQ5Zj3whzZRsLSxN9CkKqzjNQ3kjKeEacjj3OB5ufBvRP/Yg1nO4omQwg0rpbvgkQrhE5E1l9HhoNSde6Yp8mwq0RC8pj5Hr9tYrom1G92HoP/KrsK0Ygb+9tSH1VNfDJrXxKkD3Z04tqMML2r2D3tTcDO//iWL7bju0nnx+jZhBNTTkQf3dWxTS6CoWpo24WFbufQE7X66xHB5KEhVVddjKWSFt3cJE= nikita@MacBook-Pro-Nikita.local'
        },
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
    sdk: SDK = yandexcloud.SDK(service_account_key=sa_key)
    instance_service = sdk.client(InstanceServiceStub)
    operation = instance_service.Delete(
        DeleteInstanceRequest(instance_id=instance_id))

    operation_result = sdk.wait_operation_and_get_result(
        operation,
        response_type=Instance,
        meta_type=DeleteInstanceMetadata,
    )

    return MessageToDict(operation_result.response)
