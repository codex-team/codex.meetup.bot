from telegram import Update
from telegram.ext import CallbackContext

from src.services.database import database
from src.services.dns_controller import dns_controller
from src.services.servers_controller import servers_controller
from src.utils.smth_else_handler import smth_else_handler


def delete_my_server(update: Update, _: CallbackContext):
    query = update.callback_query

    server = database.servers.find_one({'userId': query.from_user.id})

    if server:
        text = 'Удаляем серверочек...'
        query.edit_message_text(text)
        servers_controller.delete_server_by_user_id(query.from_user.id)
        dns_controller.delete_record_by_user_id(query.from_user.id)
        query.edit_message_text('Сервер удалён')
    else:
        query.edit_message_text('Не найдено серверов, привязанных к вашему аккаунту')

    smth_else_handler(update)
