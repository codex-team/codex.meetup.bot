from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from src.services.database import database
from src.services.env import PARTICIPANT_LIMIT
from src.utils.keyboard import get_keyboard_for_meetup_registration


def confirm_participation(update: Update, _: CallbackContext):
    query = update.callback_query

    participate_count = database.users.count_documents({'is_registered': True})

    if participate_count > PARTICIPANT_LIMIT:
        update.callback_query.message.reply_text('К сожалению, лимит участников исчерпан :(\nПриходите в следующий раз!')
        return

    database.users.update_one(
        {'id': query.from_user.id},
        {'$set': {'is_registered': True}}
    )

    message = """
Вы зарегистрированы. 

Ждём вас 15го июля в 19:00 в ИТМО на Песочной набережной 14, ауд. 308.

Для участия вам потребуется ноутбук с установленным Ansible.
    """
    user = update.callback_query.from_user
    keyboard = get_keyboard_for_meetup_registration(user)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(message, reply_markup=reply_markup)
