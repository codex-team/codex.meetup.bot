from telegram import Update
from telegram.ext import CallbackContext
import namesgenerator

from src.services.cloudflare import create_dns_record
from src.services.database import database
from src.services.env import YANDEX_CLOUD_FOLDER_ID, CLOUDFLARE_ZONE
from src.services.yandex_cloud import create_instance


def get_server(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text('Creating server...')

    generated_name = query.from_user.username or namesgenerator.get_random_name(sep="-")
    server_name = f'{generated_name}-server'

    server_data = create_instance(YANDEX_CLOUD_FOLDER_ID, 'ru-central1-a', server_name, None)

    query.edit_message_text('Server created successfully. Obtaining domain name')

    ip_address = server_data['networkInterfaces'][0]['primaryV4Address']['oneToOneNat']['address']
    server_data['userId'] = query.from_user.id
    domain_name = f'{generated_name}.{CLOUDFLARE_ZONE}'
    created_domain_name = create_dns_record(domain_name, ip_address)
    created_domain_name['userId'] = query.from_user.id

    database.servers.insert_one(server_data)
    database.domain_names.insert_one(created_domain_name)

    query.edit_message_text('Domain name successfully created: ' + domain_name)
