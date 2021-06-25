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

    message = list(map(get_server_info_str, servers))

    query.edit_message_text('\n'.join(message))

    smth_else_handler(update)
