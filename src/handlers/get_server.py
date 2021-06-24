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

    existing_server = database.servers.find_one({'userId': query.from_user.id})

    if existing_server:
        query.edit_message_text('К вашему аккаунту уже привязан сервер')
        return

    text = 'Инициализируем сервер...'
    query.edit_message_text(text)

    generated_name = query.from_user.username or namesgenerator.get_random_name(sep="-")
    server_name = f'{generated_name}-server'

    server_data = create_instance(YANDEX_CLOUD_FOLDER_ID, 'ru-central1-a', server_name, None)

    text = text + '\nСервер успешно создан. Выделяем доменное имя...'
    query.edit_message_text(text)

    ip_address = server_data['networkInterfaces'][0]['primaryV4Address']['oneToOneNat']['address']
    server_data['userId'] = query.from_user.id
    domain_name = f'{generated_name}.{CLOUDFLARE_ZONE}'
    created_domain_name = create_dns_record(domain_name, ip_address)
    created_domain_name['userId'] = query.from_user.id

    database.servers.insert_one(server_data)
    database.domain_names.insert_one(created_domain_name)

    text = text + '\nСервер успешно создан:'
    query.edit_message_text(text)
