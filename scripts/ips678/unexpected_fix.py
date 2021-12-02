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

more_syntax = 0

records = client[db]['CleanedCommands'].find()
for record in records:
    if record["type"] == "unexpected error":
        response_string = json.dumps(record["response"]["response"])
        if "error_message" in response_string:
            if "is not defined" in response_string:
                more_syntax+=1
                record["type"] = "syntax error"
            client[db]['CleanedCommands'].update_one(
                {"_id": record["_id"]},
                {
                    "$set": {
                        "type": record["type"]
                    }
                }
            )

print(more_syntax)

