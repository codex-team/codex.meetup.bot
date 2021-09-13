from src.bot import bot
from src.services.database import database
from src.services.env import BROADCAST_TEST_MODE

message = """
Сегодня открывается набор в CodeX Lab — это наш совместный проект с Университетом ИТМО для всех, кто хочет поработать над созданием и запуском полноценных IT продуктов в команде энтузиастов. А еще это возможность попасть в основной состав Кодекса в этом сезоне. Будет сложно, но интересно.

Подробности тут: codex.so/lab.
"""

if __name__ == '__main__':
    query = {"is_admin": True} if BROADCAST_TEST_MODE else {"is_registered": True}
    for user in database.users.find(query):
        bot.sendMessage(user.get("id"), text=message)
