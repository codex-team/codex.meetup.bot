from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from src.services.database import database


def start(update: Update, _: CallbackContext) -> None:
    keyboard = [
        [
            '/get_server'
        ],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard)

    user = update.message.from_user
    query = {'id': user.id}
    database.users.update_one(query, {'$set': user.to_dict()}, upsert=True)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
