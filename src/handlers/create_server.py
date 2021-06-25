from telegram import Update
from telegram.ext import CallbackContext
import namesgenerator
from src.services.database import database
from src.services.dns_controller import dns_controller
from src.services.env import CLOUDFLARE_ZONE
from src.services.servers_controller import servers_controller
from src.utils.smth_else_handler import smth_else_handler


def get_server(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    existing_server = database.servers.find_one({'userId': query.from_user.id})

    if existing_server:
        query.edit_message_text('К вашему аккаунту уже привязан сервер')
        smth_else_handler(update)
        return

    text = 'Инициализируем сервер 🔄'
    query.edit_message_text(text)

    generated_name = (query.from_user.username or namesgenerator.get_random_name(sep="-")).replace("_", "-")

    server_data = servers_controller.create_server(query.from_user.id, f'{generated_name}-server')

    text = """
Инициализируем сервер ✅
Выделяем доменное имя 🔄
    """
    query.edit_message_text(text)

    ip_address = server_data['networkInterfaces'][0]['primaryV4Address']['oneToOneNat']['address']
    domain_name = f'{generated_name}.{CLOUDFLARE_ZONE}'

    dns_controller.create_record(query.from_user, generated_name, ip_address)

    text = f"""
Сервер готов:
IP-адрес: `{ip_address}`
Домен: {domain_name} 
SSH: `ssh root@{ip_address}`
Пароль: `{server_data.get('password')}`
    """
    query.edit_message_text(text)

    smth_else_handler(update)
