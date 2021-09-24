import pymongo
import urllib
from flask import Flask, request, jsonify

from services.properties import MONGODB_URL, DB_NAME
from services.secrets import MONGODB_PASSWORD

""" Service to access Mongo DB Cluster """

client = pymongo.MongoClient(MONGODB_URL.format(password = urllib.parse.quote_plus(MONGODB_PASSWORD)))
db = client[DB_NAME]

def insert_one(collection, document):
    return db[collection].insert_one(document)

def get_db_instance():
    return db

def find(input_email):
    record = db.User.find_one({"email": input_email})
    if record:
        return True
    else:
        return False