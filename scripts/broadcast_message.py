from src.bot import bot
from src.services.database import database
from src.services.env import BROADCAST_TEST_MODE

message = """
Привет.

Были рады видеть каждого на прошедшем митапе. Все исходники можно скачать с GitHub: https://github.com/codex-team/ansible-meetup

Анонсы предстоящих мероприятий CodeX будут публиковаться в группе https://vk.com/codex_team.

Ждем вас снова.
"""

if __name__ == '__main__':
    query = {"is_admin": True} if BROADCAST_TEST_MODE else {"is_registered": True}
    for user in database.users.find(query):
        bot.sendMessage(user.get("id"), text=message)
