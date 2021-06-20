import logging

from src.services.env import TOKEN
from telegram.ext import CommandHandler, Updater
from src.handlers.get_server import get_server
from src.handlers.start import start

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    updater = Updater(token=TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('get_server', get_server))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
