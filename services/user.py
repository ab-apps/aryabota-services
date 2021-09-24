from flask import Flask, request
from services.mongodb import insert_one, find

import json

app = Flask(__name__)

def create(record):
    input = {"email": record['email'],
            "age": record['age'],
            "python_programming_experience": record['python_programming_experience']}
    insert_one("User",input)
    return "True"

def exists(email):
    return find(email)