from telegram import Update

from src.services.database import database
from src.services.dns_controller import dns_controller
from src.services.servers_controller import servers_controller
from src.utils.smth_else_handler import smth_else_handler


def delete_all_servers(update: Update, context):
    update.callback_query.message.edit_text('Удаляю сервера и домены')

    for server in database.servers.find():
        servers_controller.delete_server_by_id(server['id'])

    for domain in database.domain_names.find():
        dns_controller.delete_record_by_id(domain['id'])
    update.callback_query.message.reply_text('Всё готово')

    smth_else_handler(update)
