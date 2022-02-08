import pymongo
import urllib
import ssl
import json

MONGODB_URL = "mongodb+srv://admin:{password}@aryabota-db-cluster.kbxud.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
MONGODB_PASSWORD = "stressbots@123"

""" Service to access Mongo DB Cluster """

client = pymongo.MongoClient(MONGODB_URL.format(password = urllib.parse.quote_plus(MONGODB_PASSWORD)),ssl_cert_reqs=ssl.CERT_NONE)

db = 'IPS678'
count = 1
records = client[db]['CleanedCommands'].find()
for record in records:
    ptype = record["type"]
    if ptype in ["syntax error", "unexpected error"]:
        print("----")
        print(count)
        count += 1
        print(ptype)
        print(record["commands"])