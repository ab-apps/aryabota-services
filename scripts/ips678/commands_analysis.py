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

syntax=0
unexpected=0
obstacle=0
correct=0
wrong=0
total=0

# first pass to find errors
records = client[db]['CleanedCommands'].find()
for record in records:
    response = record["response"]["response"]
    record["type"] = "not submitted"
    for change in response:
        if "error_message" in change:
            if "obstacle" in change["error_message"]:
                obstacle+=1
                record["type"] = "obstacle error"
            elif "syntax" in change["error_message"]:
                syntax+=1
                record["type"] = "syntax error"
            else:
                unexpected+=1
                record["type"] = "unexpected error"
        client[db]['CleanedCommands'].update_one(
            {"_id": record["_id"]},
            {
                "$set": {
                    "type": record["type"]
                }
            }
        )

# second pass to evaluate whether submitted and correct
records = client[db]['CleanedCommands'].find()
for record in records:
    total+=1
    response = record["response"]["response"]
    if record["type"] == "not submitted": 
        for change in response:
            if "succeeded" in change:
                if change["succeeded"] == True:
                    correct+=1
                    record["type"] = "correct"
                else:
                    wrong+=1
                    record["type"] = "wrong"
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