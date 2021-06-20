from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.states import State
from src.services.database import database


def start(update: Update, _: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Get list of servers", callback_data=State.GET_SERVERS_LIST.name),
            InlineKeyboardButton("Get server", callback_data=State.GET_SERVER.name),
            InlineKeyboardButton("Delete all servers", callback_data=State.DELETE_ALL_SERVERS.name),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    user = update.message.from_user
    query = {'id': user.id}
    database.users.update_one(query, {'$set': user.to_dict()}, upsert=True)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
