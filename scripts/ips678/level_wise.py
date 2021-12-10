import pymongo
import urllib
import ssl
import datetime
import pytz
import json

MONGODB_URL = "mongodb+srv://admin:{password}@aryabota-db-cluster.kbxud.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
MONGODB_PASSWORD = "stressbots@123"

""" Service to access Mongo DB Cluster """

client = pymongo.MongoClient(MONGODB_URL.format(password = urllib.parse.quote_plus(MONGODB_PASSWORD)),ssl_cert_reqs=ssl.CERT_NONE)

db = 'IPS678'

utc=pytz.UTC

current_time = datetime.datetime.now() - datetime.timedelta(days = 2)
current_time = utc.localize(current_time)

levels = ['0.0', '0.1', '0.2', '0.3', '1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2']

for level in levels:
    print(level)
    records = client[db]['CleanedCommands'].find({ "level": level })
    details = {
        "level": level,
        "correct": 0,
        "wrong": 0,
        "syntax error": 0,
        "obstacle error": 0,
        "unexpected error": 0,
        "not submitted": 0,
        "correct_answers_by": [],
        "is": 0,
        "=": 0,
        "(": 0,
        ")": 0
    }
    for record in records:
        details[record["type"]] += 1
        commands = record["commands"]
        details["is"] += commands.count(" is ")
        details["="] += commands.count("=")
        details["("] += commands.count("(")
        details[")"] += commands.count(")")
        bracket_exists = False
        if commands.count("("):
            bracket_exists = True
        if commands.count(")"):
            bracket_exists = True
        if bracket_exists:
            print(record["email"])
            print(commands)
            print("--------------")
        if record["type"] == "correct" and record["email"] not in details["correct_answers_by"]:
            details["correct_answers_by"].append(record["email"])
            
    # client[db]['LevelWiseDetails'].insert_one(details)
        

