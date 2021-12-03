import pymongo
import urllib
import ssl

MONGODB_URL = "mongodb+srv://admin:{password}@aryabota-db-cluster.kbxud.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
MONGODB_PASSWORD = "stressbots@123"

""" Service to access Mongo DB Cluster """

client = pymongo.MongoClient(MONGODB_URL.format(password = urllib.parse.quote_plus(MONGODB_PASSWORD)),ssl_cert_reqs=ssl.CERT_NONE)

db = 'IPS678'


'''To find all unique users'''
records = client[db]['CleanedCommands'].find()
for record in records:
    if not record["email"] in ["Prerna", "demo", "teacher", "teacher1", "teacher 1"]:
        user_record = client[db]['CleanedUser'].find_one({'email': record['email']})
        record['class'] = user_record['field-divided']
        client[db]['CleanedCommands'].update_one(
            {"_id": record["_id"]},
            {
                "$set": {
                    "class": record["class"]
                }
            }
        )
