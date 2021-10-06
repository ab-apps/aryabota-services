import yaml
import json
import logging

from services.arya_bota import AryaBota
from services.grid import Grid
from services.utils import get_for_every_position

""" Problem Service """

def get_initial_state(problem):
    """Return intial state of problem"""
    problem_details = problem["problem"]
    grid = Grid.get_instance()
    bot = AryaBota.get_instance()
    grid_state = grid.get_state()
    arya_bota_state = bot.get_state()
    grid_state.update(arya_bota_state)
    problem_type = problem_details["problem_type"]
    grid_state["type"] = problem_type
    return grid_state

def setup_grid_and_bot(problem):
    """Initialise the state of the grid"""
    problem_details = problem["problem"]
    problem_type = problem_details["problem_type"]
    statement = problem_details["statement"]
    problem_spec = problem_details["problem_spec"]
    state = problem["initial_state"]
    bot = AryaBota.get_instance()
    arya_bota_state = state["arya_bota"]
    if "pen" in arya_bota_state:
        bot.configure(arya_bota_state["position"]["row"], arya_bota_state["position"]["column"], arya_bota_state["dir"], arya_bota_state["pen"])
    else:
        bot.configure(arya_bota_state["position"]["row"], arya_bota_state["position"]["column"], arya_bota_state["dir"], "down")
    answer = problem["answer"]
    grid = Grid.get_instance()
    grid_state = state["grid"]
    rows = grid_state["dimensions"]["row"]
    columns = grid_state["dimensions"]["column"]
    coins_per_position = obstacles_per_position = None
    if "coins" in grid_state:
        coins_per_position = get_for_every_position(grid_state["coins"], rows, columns)
    else:
        grid_state["coins"] = None
    if "obstacles" in grid_state:
        obstacles_per_position = get_for_every_position(grid_state["obstacles"], rows, columns, False)
    else:
        grid_state["obstacles"] = None
    if not "homes" in grid_state:
        grid_state["homes"] = None
    grid.configure(rows, columns, grid_state["coins"], coins_per_position, grid_state["obstacles"], obstacles_per_position, grid_state["homes"], statement, problem_spec, problem_type, answer)

def initialise(problem_file_path):
    """Initialises chosen problem"""
    # Read problem
    with open(problem_file_path) as problem_file:
        problem = json.loads(problem_file.read())
    setup_grid_and_bot(problem)
    return get_initial_state(problem)

def render(level):
    """ Renders selected problem grid """
    with open('config.yaml') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        problem_file_path = config['levels'][level]['file']
        problem_name = config['levels'][level]['name']
    logging.info(f'Setting problem to {problem_name}')
    return initialise(problem_file_path)
