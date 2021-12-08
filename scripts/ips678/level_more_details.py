import pymongo
import urllib
import ssl

MONGODB_URL = "mongodb+srv://admin:{password}@aryabota-db-cluster.kbxud.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
MONGODB_PASSWORD = "stressbots@123"

""" Service to access Mongo DB Cluster """

client = pymongo.MongoClient(MONGODB_URL.format(password = urllib.parse.quote_plus(MONGODB_PASSWORD)),ssl_cert_reqs=ssl.CERT_NONE)

db = 'IPS678'

levels = client[db]['LevelWiseDetails'].find()
for entry in levels:
    level = entry["level"]
    entry["is"] = 0
    entry["="] = 0
    records = client[db]['CleanedCommands'].find({ "level": level })
    for record in records:
        commands = record["commands"]
        entry["is"] += commands.count(" is ")
        entry["="] += commands.count("=")
    print(level)
    print(entry)
