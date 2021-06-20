import logging

from src.handlers.start import start
from src.handlers.get_servers_list import get_servers_list
from src.handlers.get_server import get_server
from src.handlers.delete_all_servers import delete_all_servers
from src.services.env import TOKEN
from telegram.ext import CommandHandler, Updater, CallbackQueryHandler
from src.states import State

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    updater = Updater(token=TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('menu', start))
    dispatcher.add_handler(CallbackQueryHandler(get_servers_list, pattern=State.GET_SERVERS_LIST.pattern()))
    dispatcher.add_handler(CallbackQueryHandler(get_server, pattern=State.GET_SERVER.pattern()))
    dispatcher.add_handler(CallbackQueryHandler(delete_all_servers, pattern=State.DELETE_ALL_SERVERS.pattern()))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
