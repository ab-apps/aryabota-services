"""Flask App"""
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import logging
import time
import json
import yaml

from lexer_parser import understand
from services import user, problem, mongodb, properties

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s-%(funcName)s-%(asctime)s: %(message)s")

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
    """ Create and Exists operations for User """
    if request.method == 'GET':
        # Checking if user exists
        email = request.args.get('email')
        if user.exists(email):
            return jsonify(True)
        return jsonify(False)
    if request.method == 'POST':
        # Storing user survey details
        record = json.loads(request.data)
        return jsonify(user.create(record))

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
        level = request.json['level']
        problem.render(level)
        user_email = request.json['email']
        commands = request.json['commands']
        response = understand(commands)
        to_log = {
            "email": user_email,
            "timestamp": str(time.time()),
            "commands": commands,
            "response": response
        }
        logging.info(f'Received commands and executed to get response: {to_log}')
        mongodb.insert_one(properties.COMMANDS_COLLECTION, to_log)
        return jsonify(response)

# Level Endpoint
@app.route('/api/level', methods = ['GET'])
@cross_origin()
def level_endpoint():
    """Get levels list for space """
    if request.method == 'GET':
        levels_list = list()
        space = request.args.get('space')
        with open('config.yaml') as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
            levels = config['levels']
            for level in levels:
                if space in levels[level]['space']:
                    levels_list.append(level)
            return jsonify(levels_list)