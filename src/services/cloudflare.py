import CloudFlare

from src.services.env import CLOUDFLARE_TOKEN, CLOUDFLARE_ZONE_ID

cf = CloudFlare.CloudFlare(token=CLOUDFLARE_TOKEN)


def create_dns_record(name, content):
    dns_record = {
        'name': name,
        'content': content,
        'type': 'A',
    }
    return cf.zones.dns_records.post(CLOUDFLARE_ZONE_ID, data=dns_record)


def delete_dns_record(identifier):
    return cf.zones.dns_records.delete(CLOUDFLARE_ZONE_ID, identifier)
