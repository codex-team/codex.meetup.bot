from telegram.utils.request import Request
from src.services.env import TOKEN
from telegram.ext import Defaults, ExtBot

defaults = Defaults(run_async=True, parse_mode='Markdown')
bot = ExtBot(token=TOKEN, request=Request(con_pool_size=8))
bot.defaults = defaults
