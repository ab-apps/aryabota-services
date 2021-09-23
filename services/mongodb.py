import pymongo
import urllib

from services.properties import MONGODB_URL, DB_NAME
from services.secrets import MONGODB_PASSWORD

""" Service to access Mongo DB Cluster """

client = pymongo.MongoClient(MONGODB_URL.format(password = urllib.parse.quote_plus(MONGODB_PASSWORD)))
db = client[DB_NAME]

def insert_one(collection, document):
    return db[collection].insert_one(document)
