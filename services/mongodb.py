import pymongo
import urllib
from flask import Flask, request, jsonify

from services.properties import MONGODB_URL
from services.secrets import MONGODB_PASSWORD

""" Service to access Mongo DB Cluster """

client = pymongo.MongoClient(MONGODB_URL.format(password = urllib.parse.quote_plus(MONGODB_PASSWORD)))

def insert_one(db, collection, document):
    return client[db][collection].insert_one(document)

def find(db, collection, input_email):
    record = client[db][collection].find_one({"email": input_email})
    if record:
        return True
    else:
        return False
