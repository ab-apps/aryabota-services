class_mappings = {
    "problem.problem_type": {
        "class": "problem",
        "attribute_name": "type"
    },
    "problem.statement": {
        "class": "problem",
        "attribute_name": "statement"
    },
    "problem.answer": {
        "class": "problem",
        "attribute_name": "answer"
    },
    "initial_state.grid.dimensions.row": {
        "class": "grid",
        "attribute.name": "rows"
    },
    "initial_state.grid.dimensions.column": {
        "class": "grid",
        "attribute.name": "columns"
    },
    "initial_state.grid.homes": {
        "class": "grid",
        "attribute.name": "homes",
        "default": []
    },
    "initial_state.grid.obstacles": {
        "class": "grid",
        "attribute.name": "obstacles",
        "default": []
    },
    "initial_state.aryabota.position.row": {
        "class": "aryabota",
        "attribute_name": "row"
    },
    "initial_state.aryabota.position.column": {
        "class": "aryabota",
        "attribute_name": "column"
    },
    "initial_state.aryabota.dir": {
        "class": "aryabota",
        "attribute_name": "dir",
        "default": "down"
    },
    "initial_state.aryabota.pen": {
        "class": "aryabota",
        "attribute_name": "pen",
        "default": "down"
    }
}