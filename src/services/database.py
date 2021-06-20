import pymongo

from src.services.env import MONGODB_URI

client = pymongo.MongoClient(MONGODB_URI)

database = client.get_default_database() or client.meetup_bot
