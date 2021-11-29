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

total = 0
valid_records = []

records = client[db]['Commands'].find()
for record in records:
    if record["commands"].strip() == "":
        print(record["email"])
    elif record["email"] in ["Prerna", "demo", "teacher"]:
        print(record["commands"])
    else:
        total+=1
        valid_records.append(record)

print(total)

for record in valid_records:
    client[db]['CleanedCommands'].insert_one(record)