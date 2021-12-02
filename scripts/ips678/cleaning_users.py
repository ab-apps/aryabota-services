import pymongo
import urllib
import ssl

MONGODB_URL = "mongodb+srv://admin:{password}@aryabota-db-cluster.kbxud.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
MONGODB_PASSWORD = "stressbots@123"

""" Service to access Mongo DB Cluster """

client = pymongo.MongoClient(MONGODB_URL.format(password = urllib.parse.quote_plus(MONGODB_PASSWORD)),ssl_cert_reqs=ssl.CERT_NONE)

db = 'IPS678'

# Generating Cleaned User DB

all_users = dict()

'''To find all unique users'''
records = client[db]['User'].find()
for record in records:
    if record["email"] not in  ["Prerna", "demo", "teacher", "teacher 1", "teacher1"]:
        if record["email"] not in all_users:
            all_users[record["email"]] = record
        else:
            print(record)
            print(all_users[record["email"]])
            if record['email'] == 'attyaksh676320' or "sakshamlohan" in record["email"]:
                all_users[record['email']] = record
            if record['email'] == '7519':
                all_users[record['email']]['skills'] = record['skills']

# cleaning field-divided                
for email in all_users:
    print(all_users[email])
    if 'field-divided' in all_users[email]:
        field_divided = all_users[email]["field-divided"]
        if '8' in field_divided:
            field_divided = '8'
        elif '6' in field_divided:
            field_divided = '6'
        elif '7' in field_divided:
            field_divided = '7'
        else:
            field_divided = 'unknown'
    else:
        field_divided = 'unknown'
    all_users[email]["field-divided"] = field_divided

for email in all_users:
    client['IPS678']['CleanedUser'].insert_one(all_users[email])

print(len(all_users))