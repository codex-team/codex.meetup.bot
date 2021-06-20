from telegram import Update
from telegram.ext import CallbackContext
import namesgenerator

from src.services.cloudflare import create_dns_record
from src.services.env import YANDEX_CLOUD_FOLDER_ID, CLOUDFLARE_ZONE
from src.services.yandex_cloud import create_instance


def get_servers_list(update: Update, _: CallbackContext) -> None:
    query = update.callback_query

    query.answer()
