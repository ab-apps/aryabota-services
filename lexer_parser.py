"""Lexer and parser module for pseudo-code"""
# pylint: disable=invalid-name,unused-argument,global-statement
import json
import yaml
import logging

from control_hub import *
from services.grid import Grid
from services.arya_bota import AryaBota
from services.utils import get_custom_error
from lexers.stage1 import stage1_lexer
from lexers.stage2 import stage2_lexer

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

bot = AryaBota.get_instance()
grid = Grid.get_instance()

def run_lexer(commands, lexer):
    tokens = []
    lexer.input(commands)
    token = lexer.token()
    while token is not None:
        tokens.append(token.value)
        token = lexer.token()
    commands = "".join(tokens)
    return commands

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
                commands = commands.replace("    ", "\t")
                commands = commands.strip("\n")
                commands = commands.replace("\r"," ")
                print(commands)
                post_stage1_commands = run_lexer(commands, stage1_lexer)
                python_program = run_lexer(post_stage1_commands, stage2_lexer)
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
            exception_raised = get_custom_error(e)
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