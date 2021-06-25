from time import sleep

from telegram import InlineKeyboardMarkup, Update

from src.utils.keyboard import get_keyboard_for_user


def smth_else_handler(update: Update):
    sleep(2)
    query = update.callback_query

    keyboard = get_keyboard_for_user(query.from_user)

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Что-то ещё?', reply_markup=reply_markup)
