from src.services.database import database
from src.services.yandex_cloud import delete_instance


def delete_all_servers(update, context):
    for server in database.servers.find():
        try:
            delete_instance(server['id'])
        except Exception:
            pass
        finally:
            database.servers.remove({'id': server['id']})
