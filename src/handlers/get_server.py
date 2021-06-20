from telegram import Update
from telegram.ext import CallbackContext
import namesgenerator

from src.services.cloudflare import create_dns_record
from src.services.env import YANDEX_CLOUD_FOLDER_ID, CLOUDFLARE_ZONE
from src.services.yandex_cloud import create_instance


def get_server(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Creating server...')

    generated_name = update.message.from_user.username or namesgenerator.get_random_name(sep="-")

    server_name = f'{generated_name}-server'

    server_data = create_instance(YANDEX_CLOUD_FOLDER_ID, 'ru-central1-a', server_name, None)

    update.message.reply_text('Server created successfully. Obtaining domain name')

    ip_address = server_data.network_interfaces[0].primary_v4_address.one_to_one_nat.address

    domain_name = f'{generated_name}.{CLOUDFLARE_ZONE}'
    create_dns_record(domain_name, ip_address)

    update.message.reply_text('Domain name successfully created: ' + domain_name)

