from telegram import Update
from telegram.ext import CallbackContext
from src.services.database import database
from src.utils.smth_else_handler import smth_else_handler


def get_server_info_str(server):
    ip_address = server['networkInterfaces'][0]['primaryV4Address']['oneToOneNat']['address']
    return f'`ssh root@{ip_address}` | `{server.get("password")}`'


def get_servers_list(update: Update, _: CallbackContext) -> None:
    query = update.callback_query

    query.answer()

    servers = database.servers.find({})

    messages = list(map(get_server_info_str, servers))

    message = '\n'.join(messages) if len(messages) > 0 else 'Серверов не найдено'

    query.edit_message_text(message)

    smth_else_handler(update)
