from telegram import Update
from telegram.ext import CallbackContext

from src.services.database import database


def reject_participation(update: Update, _: CallbackContext):
    query = update.callback_query

    database.users.update_one(
        {'id': query.from_user.id},
        {'$set': {'is_registered': False}}
    )

    update.callback_query.message.reply_text("""
Ждём вас на следующем митапе. Если захотите все-таки принять участие, введите команду /start 
    """)
    query.edit_message_reply_markup(None)
