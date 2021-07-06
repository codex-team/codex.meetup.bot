from pymongo import ReturnDocument
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.services.env import PRE_REGISTRATION_MODE
from src.utils.keyboard import get_keyboard_for_user
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
        if PRE_REGISTRATION_MODE:
            update.message.reply_text('Возможность управлять серверами отключена')
            return
        keyboard = get_keyboard_for_user(user)

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Действия администратора:', reply_markup=reply_markup)
        return

    if founded_user.get('is_registered', False):
        if PRE_REGISTRATION_MODE:
            update.message.reply_text("""
Вы уже зарегистрирован. 

Ждём вас 15го июля в 19:00 в корпусе ИТМО на Песочной набережной д.14, ауд. 308.

Не забудьте взять ноутбук с предварительно установленным Ansible.
            """)
            return

        keyboard = get_keyboard_for_user(user)

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Выберите действие:', reply_markup=reply_markup)
    else:
        keyboard = get_keyboard_for_user(user)

        reply_markup = InlineKeyboardMarkup(keyboard)

        welcome_text = """
Привет.

Я помогу зарегистрироваться на CodeX Meetup: Ansible.

Митап пройдёт 15го июля в 19:00 в ИТМО на Песочной набережной 14, ауд. 308. Вам потребуется ноутбук с установленным Ansible.

Нажмите на кнопку, чтобы подтвердить участие.
        """

        update.message.reply_text(welcome_text, reply_markup=reply_markup)
