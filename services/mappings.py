# Attribute Constants
PROBLEM_TYPE = "problem_type"
STATEMENT = "statement"
ANSWER = "answer"
ROWS = "rows"
COLUMNS = "columns"
HOMES = "homes"
OBSTACLES = "obstacles"
COINS = "coins"
COLOURED = "coloured"
ROW = "row"
COLUMN = "column"
DIR = "dir"
PEN = "pen"

# Schema Constants
POSITION = "position"
NUMBER = "number"

# Attribute Mappings
attributes = {
    "problem.problem_type": {
        "class": "Problem",
        "attribute_name": PROBLEM_TYPE
    },
    "problem.statement": {
        "class": "Problem",
        "attribute_name": STATEMENT
    },
    "answer": {
        "class": "Problem",
        "attribute_name": ANSWER,
        "default": None
    },
    "initial_state.grid.dimensions.row": {
        "class": "Grid",
        "attribute_name": ROWS
    },
    "initial_state.grid.dimensions.column": {
        "class": "Grid",
        "attribute_name": COLUMNS
    },
    "initial_state.grid.homes": {
        "class": "Grid",
        "attribute_name": HOMES,
        "default": []
    },
    "initial_state.grid.obstacles": {
        "class": "Grid",
        "attribute_name": OBSTACLES,
        "default": []
    },
    "initial_state.grid.coins": {
        "class": "Grid",
        "attribute_name": COINS,
        "default": []
    },
    "initial_state.grid.coloured": {
        "class": "Grid",
        "attribute_name": COLOURED,
        "default": []
    },
    "initial_state.arya_bota.position.row": {
        "class": "AryaBota",
        "attribute_name": ROW
    },
    "initial_state.arya_bota.position.column": {
        "class": "AryaBota",
        "attribute_name": COLUMN
    },
    "initial_state.arya_bota.dir": {
        "class": "AryaBota",
        "attribute_name": DIR,
        "default": "down"
    },
    "initial_state.arya_bota.pen": {
        "class": "AryaBota",
        "attribute_name": PEN,
        "default": "down"
    }
}