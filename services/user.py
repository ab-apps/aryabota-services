from flask import Flask, request
from services.mongodb import insert_one, find

import json

app = Flask(__name__)

def create(record):
    insert_one("User", record)
    return True

def exists(email):
    return find("User", email)