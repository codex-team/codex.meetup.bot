from telegram import Update
from telegram.ext import CallbackContext
from src.services.database import database
from src.services.env import PARTICIPANT_LIMIT


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

    update.callback_query.message.reply_text('Вы успешно зарегистрированы на митап. Ждём вас 15го июля в 19:00 в '
                                             'корпусе ИТМО на Песочной набережной д.14, ауд. 308.')
    query.edit_message_reply_markup(None)