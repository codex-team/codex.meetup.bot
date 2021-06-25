from telegram import InlineKeyboardButton, User

from src.services.database import database
from src.states import State


def get_keyboard_for_user(tg_user: User):
    user = database.users.find_one({'id': tg_user.id})
    if user.get('is_admin', False):
        keyboard = [
            [InlineKeyboardButton("Список серверов", callback_data=State.GET_SERVERS_LIST.name)],
            [InlineKeyboardButton("Получить сервер", callback_data=State.GET_SERVER.name)],
            [InlineKeyboardButton("Удалить все сервера", callback_data=State.DELETE_ALL_SERVERS.name)],
            [InlineKeyboardButton("Удалить мой сервер", callback_data=State.DELETE_MY_SERVER.name)]
        ]

        return keyboard

    if user.get('is_registered', False):
        keyboard = [
            [
                InlineKeyboardButton("Получить сервер", callback_data=State.GET_SERVER.name),
                InlineKeyboardButton("Удалить мой сервер", callback_data=State.DELETE_MY_SERVER.name),
            ]
        ]

        return keyboard
    else:
        keyboard = [
            [
                InlineKeyboardButton("Хочу на митап!", callback_data=State.CONFIRM_PARTICIPATION.name),
            ]
        ]

        return keyboard
