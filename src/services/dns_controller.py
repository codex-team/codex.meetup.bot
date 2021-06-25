from src.services.cloudflare import create_dns_record, delete_dns_record
from src.services.database import database


class DnsController:
    def create_record(self, user, name, ip_address):
        created_domain_name = create_dns_record(name, ip_address)
        created_domain_name['userId'] = user.id

        database.domain_names.insert_one(created_domain_name)

    def delete_record_by_id(self, record_id):
        try:
            delete_dns_record(record_id)
        except Exception:
            pass
        finally:
            database.domain_names.remove({'id': record_id})

    def delete_record_by_user_id(self, user_id):
        record = database.domain_names.find_one({'userId': user_id})
        self.delete_record_by_id(record['id'])


dns_controller = DnsController()
