import pymongo
import urllib
import ssl
import datetime
import pytz

MONGODB_URL = "mongodb+srv://admin:{password}@aryabota-db-cluster.kbxud.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
MONGODB_PASSWORD = "stressbots@123"

""" Service to access Mongo DB Cluster """

client = pymongo.MongoClient(MONGODB_URL.format(password = urllib.parse.quote_plus(MONGODB_PASSWORD)),ssl_cert_reqs=ssl.CERT_NONE)

db = 'IPS678'

utc=pytz.UTC

current_time = datetime.datetime.now() - datetime.timedelta(days = 2)
current_time = utc.localize(current_time)

wrong = []
right = []

def check_answer(record):
    if record["type"] == "correct":
        commands = record["commands"]
        if "/" in commands:
            right.append(record["email"])
            print("---------")
            return True
        else:
            wrong.append(record["email"])
    return False

records = client[db]['CleanedCommands'].find({ "level": "1.3" })
records = list(records)
correct = sum(check_answer(record) for record in records)
print(correct)
print(wrong)
print(right)

# for record in records:
#     if record["type"] == "syntax error":
#         print(record["email"])
#         print(record["commands"])
#         print("-------")
    