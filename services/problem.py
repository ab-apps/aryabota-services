import yaml
import json
import logging

from services.singleton_classes import AryaBota, Problem
from services.singleton_classes import Grid
from services.mappings import attributes

""" Problem Service """

def get_initial_state():
    """Return intial state of problem"""
    state = Problem.get_instance().get_state()
    state.update(Grid.get_instance().get_state())
    state.update(AryaBota.get_instance().get_state())
    return state

def set_up(problem):
    """Initialise the state of the programming environment"""
    attributes_per_class = {
        "Problem": {},
        "Grid": {},
        "AryaBota": {}
    }
    for path in attributes:
        value = None
        try:
            path_string = "problem" + "".join(["['" + key + "']" for key in path.split('.')])
            value = eval(path_string)
        except KeyError:
            if "default" in attributes[path]:
                value = attributes[path]["default"]
            else:
                raise KeyError("Check the Problem Schema, required field(s) missing!")
        attributes_per_class[attributes[path]["class"]][attributes[path]["attribute_name"]] = value

    Grid.get_instance().configure(attributes_per_class["Grid"])
    AryaBota.get_instance().configure(attributes_per_class["AryaBota"])
    Problem.get_instance().configure(attributes_per_class["Problem"])            

def initialise(problem_file_path):
    """Initialises chosen problem"""
    # Read problem
    with open(problem_file_path) as problem_file:
        problem = json.loads(problem_file.read())
    set_up(problem)
    return get_initial_state()

def render(level):
    """Renders selected problem"""
    with open('config.yaml') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        problem_file_path = config['levels'][level]['file']
        problem_name = config['levels'][level]['name']
    logging.info(f'Setting problem to {problem_name}')
    return initialise(problem_file_path)
