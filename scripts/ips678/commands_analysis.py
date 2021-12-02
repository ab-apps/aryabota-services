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

syntax=0
unexpected=0
obstacle=0
correct=0
wrong=0
total=0

records = client[db]['CleanedCommands'].find()
for record in records:
    response = record["response"]["response"]
    record["type"] = "not submitted"
    response_string = json.dumps(response)
    if "error_message" in response_string:
        if "obstacle" in response_string:
            obstacle+=1
            record["type"] = "obstacle error"
        elif "syntax" in response_string:
            syntax+=1
            record["type"] = "syntax error"
        else:
            unexpected+=1
            record["type"] = "unexpected error"
    elif "Correct answer!" in response_string:
        record["type"] = "correct"
        correct+=1
    elif "Wrong answer" in response_string:
        record["type"] = "wrong"
        wrong+=1
                
    client[db]['CleanedCommands'].update_one(
        {"_id": record["_id"]},
        {
            "$set": {
                "type": record["type"]
            }
        }
    )

print(syntax)
print(obstacle)
print(unexpected)
print(correct)
print(wrong)
print(total)