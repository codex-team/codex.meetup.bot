from src.bot import bot
from src.services.database import database
from src.services.env import BROADCAST_TEST_MODE

message = """
Напоминаем, что вы зарегистрированы на Codex Meetup: Ansible, который пройдёт завтра, в 19:00 в корпусе ИТМО на Песочной набережной 14, ауд. 308. 

Для участия вам потребуется ноутбук с установленным Ansible.

Гайд по установке Ansible: https://codex.so/how-to-install-ansible.
"""

if __name__ == '__main__':
    query = {"is_admin": True} if BROADCAST_TEST_MODE else {"is_registered": True}
    for user in database.users.find(query):
        bot.sendMessage(user.get("id"), text=message)
