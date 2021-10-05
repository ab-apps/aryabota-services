from flask import Flask, request
from services.mongodb import insert_one, find

import json

app = Flask(__name__)

def create(space, record):
    insert_one(space, "User", record)
    return True

def exists(space, email):
    return find(space, "User", email)