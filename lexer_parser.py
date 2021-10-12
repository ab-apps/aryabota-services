"""Lexer and parser module for pseudo-code"""
# pylint: disable=invalid-name,unused-argument,global-statement
import json
import yaml
import logging

from control_hub import *
from services.grid import Grid
from services.coin_sweeper import CoinSweeper
from languages.english import english_lexer, english_parser

# utilities
class LexerError(Exception):
    """Lexer error"""
    # pass

def make_command(command, value = None):
    """Wrap command in JSON response format"""
    if command == "get_row()":
        return {
                "python": command,
                "value": bot.my_row()
               }
    elif command == "get_column()":
        return {
                "python": command,
                "value": bot.my_column()
               }
    elif "get_number_of_coins()" in command:
        return {
                "python": command,
                "number of coins": value
               }
    elif '+' in command or '-' in command or '*' in command or '/' in command or '=' in command:
        return {
                "python": command
               }
    elif command == "error()":
        return {
            "error_message": value,
        }
    else:
        return {
            "python": command,
            "stateChanges": [
                bot.get_state()
            ]
        }

bot = CoinSweeper.get_instance()
grid = Grid.get_instance()

def understand(commands):
    """Convert pseudo-code to Python code to execute"""
    # reinitialize response file
    # Opening config to read grid attributes
    with open('config.yaml') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        with open(config["app"]["results"], "w") as results_file:
            results_file.write(json.dumps([]))
        try:
            if config["app"]["language"] == "english":
                python_program = english_parser.parse(commands, lexer=english_lexer)
                print(python_program)
        except Exception as exception:
            logging.error(f'Exception occured', exc_info=True)
            return []
    if python_program is None:
        exception_raised = "Aryabota doesn't understand you. There might be a syntax error."
    else:
        exception_raised = None
        try:
            exec(python_program) # pylint: disable=exec-used
        except Exception as e:
            exception_raised = e
            logging.error(f'Exception while executing Python program: {e}', exc_info=True)
    with open(config["app"]["results"]) as results_file:
        response = json.loads(results_file.read())
    if exception_raised is not None:
        response.append({
            "error_message": str(exception_raised)
        })
    response_and_python_program = {
        "python": python_program,
        "response": response
    }
    print(response_and_python_program)
    return response_and_python_program