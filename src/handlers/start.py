from pymongo import ReturnDocument
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.states import State
from src.services.database import database


def start(update: Update, _: CallbackContext) -> None:
    user = update.message.from_user
    query = {'id': user.id}
    founded_user = database.users.find_one_and_update(
        query,
        {'$set': user.to_dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    if founded_user.get('is_admin', False):
        keyboard = [
            [
                InlineKeyboardButton("Список серверов", callback_data=State.GET_SERVERS_LIST.name),
                InlineKeyboardButton("Получить сервер", callback_data=State.GET_SERVER.name),
                InlineKeyboardButton("Удалить все сервера", callback_data=State.DELETE_ALL_SERVERS.name),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Действия администратора:', reply_markup=reply_markup)
        return

    if founded_user.get('is_registered', False):
        keyboard = [
            [
                InlineKeyboardButton("Получить сервер", callback_data=State.GET_SERVER.name),
                InlineKeyboardButton("Удалить мой сервер", callback_data=State.DELETE_MY_SERVER.name),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Выберите действие:', reply_markup=reply_markup)
    else:
        keyboard = [
            [
                InlineKeyboardButton("Хочу на митап!", callback_data=State.CONFIRM_PARTICIPATION.name),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        welcome_text = """
Привет!
С помощью этого бота ты можешь зарегистрироваться на наш митап по Ansible.
Нажми на кнопку, чтобы подтвердить участие
        """

        update.message.reply_text(welcome_text, reply_markup=reply_markup)
