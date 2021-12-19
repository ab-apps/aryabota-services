"""The state of the Programming Environment is maintained through these Singleton classes"""

from services.mappings import ANSWER, COINS, COLOURED, COLUMN, COLUMNS, DIR, HOMES, NUMBER, OBSTACLES, PEN, POSITION, PROBLEM_TYPE, ROW, ROWS, STATEMENT


class Grid:
    """ Grid class and its attributes """
    __instance = None
    @staticmethod
    def get_instance():
        """Static access method"""
        if Grid.__instance is None:
            Grid()
        return Grid.__instance

    def __init__(self):
        """Virtually private constructor"""
        if Grid.__instance is not None:
            raise Exception("This class is a Singleton!")
        Grid.__instance = self 
        
    def configure(self, attributes):
        # to deal with, coins and obstacles per position
        for key in attributes:
            setattr(self, key, attributes[key])
        self.coloured = []

    def colour(self, pos):
        """Colouring the trail as required"""
        if pos not in self.coloured:
            self.coloured.append(pos)

    def get_number_of_coins_at_pos(self, row, column):
        """Get number of coins at a given position in the grid, ie, (row, column)"""
        if row <= self.get(ROWS) and column <= self.get(COLUMNS):
            for i in self.get(COINS):
                if i[POSITION][ROW] == row and i[POSITION][COLUMN] == column:
                    return i[NUMBER]
        # TODO design choice: if row and column are outside the grid, do we want to raise an exception?
        return 0

    def get(self, key):
        return getattr(self, key)

    def get_state(self):
        state = {}
        for attribute in [ROWS, COLUMNS, COINS, OBSTACLES, HOMES, COLOURED]:
            state[attribute] = self.get(attribute)
        return state

    def get_state_for_answer(self):
        """Returning state for answer check"""
        if self.__instance:
            return {
                "dimensions": {
                    "row": self.rows,
                    "column": self.columns
                },
                "coins": self.coins,
                "obstacles": self.obstacles,
                "coloured": self.coloured
            }
        return {}

class AryaBota:
    """AryaBota robot and its attributes"""
    __instance = None
    @staticmethod
    def get_instance():
        """Static access method"""
        if AryaBota.__instance is None:
            AryaBota()
        return AryaBota.__instance

    def __init__(self):
        """Virtually private constructor"""
        if AryaBota.__instance is not None:
            raise Exception("This class is a singleton!")
        AryaBota.__instance = self

    def configure(self, attributes):
        for key in attributes:
            setattr(self, key, attributes[key])
        self.trail = []
        self.append_position_to_trail()

    def get(self, key):
        return getattr(self, key)

    def get_state(self):
        state = {}
        for attribute in [ROW, COLUMN, DIR, PEN]:
            state[attribute] = self.get(attribute)
        return state

    def get_state_for_answer(self):
        """Get current state of the AryaBota robot's position wrapped in a dictionary"""
        return {
            "position": {
                "row": self.row,
                "column": self.column
            }
        }

    def append_position_to_trail(self, row = None, column = None):
        GRID = Grid.get_instance()
        """Append current position to trail"""
        if row is None and column is None:
            pos = {
                "row": self.row,
                "column": self.column
            }
        else:
            pos = {
                "row": row,
                "column": column
            }
        self.trail.append(pos)
        if self.pen == "down":
            GRID.colour({
                "position": pos
            })

    # ask
    def my_row(self):
        """Get current row of the AryaBota robot"""
        return self.row

    def my_column(self):
        """Get current column of the AryaBota robot"""
        return self.column

    # affect
    def move(self, steps):
        """Move the AryaBota robot in the direction in which it is facing
        steps: specified number of steps to move it by"""
        GRID = Grid.get_instance()
        state = GRID.get_state()
        obstacle_message = "There's an obstacle, cannot move ahead"
        boundary_message = "This position does not exist on the grid!"
        if self.dir == "up" or self.dir == "down":
            curr_row = self.row
            if self.dir == "up":
                to_move = curr_row - steps
                offset = -1
            else:
                to_move = curr_row + steps
                offset = 1
            if to_move >=1 and to_move <= GRID.rows:
                for i in range(curr_row, to_move, offset):
                    curr_row  = curr_row + offset
                    pos_obj = {'position': {'row': curr_row, 'column': self.column}}
                    if pos_obj in state['obstacles']:
                        return [False, obstacle_message]
                for i in range(self.row, to_move, offset):
                    if self.pen == "down":
                        self.append_position_to_trail(i, self.column)
                self.row = curr_row
            else:
                return [False, boundary_message]
        elif self.dir == "left" or self.dir == "right":
            curr_column = self.column
            if self.dir == "right":
                to_move = curr_column + steps
                offset = 1
            else:
                to_move = curr_column - steps
                offset = -1
            if to_move >=1 and to_move <= GRID.columns:
                for i in range(curr_column, to_move, offset):
                    curr_column = curr_column + offset
                    pos_obj = {'position': {'row': self.row, 'column': curr_column}}
                    if pos_obj in state['obstacles']:
                        return [False, obstacle_message]
                for i in range(self.column, to_move, offset):
                    if self.pen == "down":
                        self.append_position_to_trail(self.row, i)
                self.column = curr_column
            else:
                return [False, boundary_message]
        return [True, "Moved!"]

    def turn_left(self):
        """Turn the AryaBota robot to its left"""
        if self.dir == "up":
            self.dir = "left"
        elif self.dir == "down":
            self.dir = "right"
        elif self.dir == "right":
            self.dir = "up"
        elif self.dir == "left":
            self.dir = "down"

    def turn_right(self):
        """Turn the AryaBota robot to its right"""
        if self.dir == "up":
            self.dir = "right"
        elif self.dir == "down":
            self.dir = "left"
        elif self.dir == "right":
            self.dir = "down"
        elif self.dir == "left":
            self.dir = "up"

    def set_pen(self, status = "up"):
        """Toggle the status of pen"""
        self.pen = status

class Problem:
    """Problem and its attributes"""
    __instance = None
    @staticmethod
    def get_instance():
        """Static access method"""
        if Problem.__instance is None:
            Problem()
        return Problem.__instance

    def __init__(self):
        """Virtually private constructor"""
        if Problem.__instance is not None:
            raise Exception("This class is a Singleton!")
        Problem.__instance = self
    
    def configure(self, attributes):
        for key in attributes:
            setattr(self, key, attributes[key])

    def get(self, key):
        return getattr(self, key)

    def get_state(self):
        state = {}
        for attribute in [PROBLEM_TYPE, STATEMENT]:
            state[attribute] = self.get(attribute)
        return state

    
