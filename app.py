"""Flask App"""
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import logging
import time
import json

from lexer_parser import understand
from services import user, problem, mongodb, properties

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG, filename="app.log", format="%(levelname)s-%(funcName)s-%(asctime)s: %(message)s")

# Endpoints
@app.route('/')
@cross_origin()
def index():
    """Hello World"""
    return "Hello World!"

# User API Endpoint
@app.route('/api/user', methods = ['POST','GET'])
@cross_origin()
def user_endpoint():
    print("User")
    """ Create and Exists operations for User """
    if request.method == 'GET':
        # Checking if user exists
        #email = request.args.get("email")
        record = json.loads(request.data)
        email = record['email']
        print(email)
        if user.exists(email):
            return jsonify(True)
        return jsonify(False)
    if request.method == 'POST':
        # Storing user survey details
        record = json.loads(request.data)
        #return jsonify(user.create(record))
        return user.create(record)

# Problem Endpoint
@app.route('/api/problem', methods = ['GET', 'POST'])
@cross_origin()
def problem_endpoint():
    """ Render specified problem grid """
    if request.method == 'GET':
        # Getting problem grid for the requested level
        level = request.args.get('level')
        return jsonify(problem.render(level))
    if request.method == 'POST':
        print('!! post', request.json)
        level = request.json['level']
        problem.render(level)
        user_email = request.json['email']
        commands = request.json['commands']
        to_log = {
            "email": user_email,
            "timestamp": str(time.time()),
            "commands": commands
        }
        logging.info(f'Received commands to execute: {to_log}')
        mongodb.insert_one(properties.COMMANDS_COLLECTION, to_log)
        response = understand(commands)
        return jsonify(response)
