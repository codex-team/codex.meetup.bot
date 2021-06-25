import logging

from telegram.utils.request import Request

from src.handlers.confirm_participation import confirm_participation
from src.handlers.delete_my_server import delete_my_server
from src.handlers.start import start
from src.handlers.get_servers_list import get_servers_list
from src.handlers.create_server import get_server
from src.handlers.delete_all_servers import delete_all_servers
from src.services.env import TOKEN, PRE_REGISTRATION_MODE
from telegram.ext import CommandHandler, Updater, CallbackQueryHandler, Defaults, ExtBot
from src.states import State

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    defaults = Defaults(run_async=True, parse_mode='Markdown')
    bot = ExtBot(token=TOKEN, request=Request(con_pool_size=8))
    bot.defaults = defaults
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(confirm_participation, pattern=State.CONFIRM_PARTICIPATION.pattern()))

    if not PRE_REGISTRATION_MODE:
        dispatcher.add_handler(CommandHandler('menu', start))
        dispatcher.add_handler(CallbackQueryHandler(get_servers_list, pattern=State.GET_SERVERS_LIST.pattern()))
        dispatcher.add_handler(CallbackQueryHandler(get_server, pattern=State.GET_SERVER.pattern()))
        dispatcher.add_handler(CallbackQueryHandler(delete_all_servers, pattern=State.DELETE_ALL_SERVERS.pattern()))
        dispatcher.add_handler(CallbackQueryHandler(delete_my_server, pattern=State.DELETE_MY_SERVER.pattern()))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
