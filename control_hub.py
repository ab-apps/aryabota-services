"""Control Hub that makes changes to the AryaBota environment - grid and robot"""
# Writes outcomes to a result file
import json
import yaml
from services.mappings import DIR
from services.singleton_classes import Grid
from services.singleton_classes import AryaBota
from services.utils import check_answer

# Opening config to read grid attributes
with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

BOT = AryaBota.get_instance()
GRID = Grid.get_instance()
results_file_path = config["app"]["results"]

def make_response(response_type, response):
    """Create a response object"""
    if response_type == "value":
        return {
            "value": response
        }
    if response_type == "state":
        return {
            "stateChanges": [response]
        }
    if response_type == "error":
        return {
            "error_message": response
        }
    if response_type == "submit":
        return response

def get_my_row():
    """return current row"""
    return BOT.my_row()

def get_my_column():
    """return current column"""
    return BOT.my_column()

def move(steps):
    """move ahead on grid"""
    (success, message) = BOT.move(steps)
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
        if success:
            results.append(make_response("state", BOT.get_state()))
        else:
            results.append(make_response("error", message))
            # TODO: add specific error raising
            raise Exception("Hitting obstacles or falling off the grid ;_;")
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))

def turn(direction = "left"):
    """turn left on grid"""
    if direction == "left":
        BOT.turn_left()
    elif direction == "right":
        BOT.turn_right()
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
        results.append(make_response("state", BOT.get_state()))
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))

def set_pen(status = "up"):
    """change pen status"""
    BOT.set_pen(status)

def get_number_of_coins(row = None, column = None):
    """return number of coins at current position"""
    if row is None:
        row = BOT.my_row()
    if column is None:
        column = BOT.my_column()
    return GRID.get_number_of_coins_at_pos(row,column)

def obstacle_ahead(row = None, column = None):
    """return if obstacle ahead"""
    if row is None:
        row = BOT.my_row()
    if column is None:
        column = BOT.my_column()
    state = GRID.get_state()
    direction = BOT.get(DIR)
    if direction == "down":
        if row+1 <= GRID.rows:
            if({'position': {'row': row+1, 'column': column}} in state['obstacles']):
                return 1
        else:
            return 1
    elif direction == "up":
        if row-1 > 0:
            if({'position': {'row': row-1, 'column': column}} in state['obstacles']):
                return 1
        else:
            return 1
    elif direction == "right":
        if column+1 <= GRID.columns:
            if({'position': {'row': row, 'column': column+1}} in state['obstacles']):
                return 1
        else:
            return 1
    elif direction == "left":
        if column-1 > 0:
            if({'position': {'row': row, 'column': column-1}} in state['obstacles']):
                return 1
        else:
            return 1
    return 0

def obstacle_behind(row = None, column = None):
    """return if obstacle behind"""
    if row is None:
        row = BOT.my_row()
    if column is None:
        column = BOT.my_column()
    state = GRID.get_state()
    direction = BOT.get(DIR)
    if direction == "up":
        if row+1 <= GRID.rows:
            if({'position': {'row': row+1, 'column': column}} in state['obstacles']):
                return 1
        else:
            return 1
    elif direction == "down":
        if row-1 > 0:
            if({'position': {'row': row-1, 'column': column}} in state['obstacles']):
                return 1
        else:
            return 1
    elif direction == "left":
        if column+1 <= GRID.columns:
            if({'position': {'row': row, 'column': column+1}} in state['obstacles']):
                return 1
        else:
            return 1
    elif direction == "right":
        if column-1 > 0:
            if({'position': {'row': row, 'column': column-1}} in state['obstacles']):
                return 1
        else:
            return 1
    return 0

def obstacle_left(row = None, column = None):
    """return if obstacle to the left"""
    if row is None:
        row = BOT.my_row()
    if column is None:
        column = BOT.my_column()
    state = GRID.get_state()
    direction = BOT.get(DIR)
    if direction == "left":
        if row+1 <= GRID.rows:
            if({'position': {'row': row+1, 'column': column}} in state['obstacles']):
                return 1
        else:
            return 1
    elif direction == "right":
        if row-1 > 0:
            if({'position': {'row': row-1, 'column': column}} in state['obstacles']):
                return 1
        else:
            return 1
    elif direction == "down":
        if column+1 <= GRID.columns:
            if({'position': {'row': row, 'column': column+1}} in state['obstacles']):
                return 1
        else:
            return 1
    elif direction == "up":
        if column-1 > 0:
            if({'position': {'row': row, 'column': column-1}} in state['obstacles']):
                return 1
        else:
            return 1
    return 0

def obstacle_right(row = None, column = None):
    """return if obstacle to the right"""
    if row is None:
        row = BOT.my_row()
    if column is None:
        column = BOT.my_column()
    state = GRID.get_state()
    direction = BOT.get(DIR)
    if direction == "right":
        if row+1 <= GRID.rows:
            if({'position': {'row': row+1, 'column': column}} in state['obstacles']):
                return 1
        else:
            return 1
    elif direction == "left":
        if row-1 > 0:
            if({'position': {'row': row-1, 'column': column}} in state['obstacles']):
                return 1
        else:
            return 1
    elif direction == "up":
        if column+1 <= GRID.columns:
            if({'position': {'row': row, 'column': column+1}} in state['obstacles']):
                return 1
        else:
            return 1
    elif direction == "down":
        if column-1 > 0:
            if({'position': {'row': row, 'column': column-1}} in state['obstacles']):
                return 1
        else:
            return 1
    return 0

def home():
    state = GRID.get_state()
    row = BOT.my_row()
    column = BOT.my_column()
    pos = {
        "position": {
            "row": row,
            "column": column
        }
    }
    if pos in state["homes"]:
        print("At home, yes")
        return True
    return False


def print_value(expr):
    """print value"""
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
    response = expr
    results.append(make_response("value", response))
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))

def submit(value = None):
    """submit answer"""
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
    if value is not None:
        response = check_answer(value)
    else:
        current_state = {
            "arya_bota": BOT.get_state_for_answer(),
            "grid": GRID.get_state_for_answer()
        }
        response = check_answer(current_state)
    results.append(make_response("submit", response))
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))
