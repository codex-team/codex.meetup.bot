from telegram import Update
from telegram.ext import CallbackContext

from src.services.database import database
from src.services.yandex_cloud import delete_instance


def delete_my_server(update: Update, _: CallbackContext):
    query = update.callback_query

    server = database.servers.find_one({'userId': query.from_user.id})

    if server:
        text = 'Удаляем серверочек...'
        server_id = server.get('id')
        query.edit_message_text(text)
        delete_instance(server_id)
        database.servers.delete_one({'id': server_id})
    else:
        query.edit_message_text('Не найдено серверов, привязанных к вашему аккаунту')
