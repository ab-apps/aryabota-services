"""the Singleton AryaBota robot, its attributes and state"""
from services.grid import Grid

GRID = Grid.get_instance()

class AryaBota:
    """AryaBota robot class
    Properties:
        row: current row (1-indexed)
        column: current column (1-indexed)
        dir: current direction the robot is facing (can be up, left, down, right)
    """
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
        self.row = 1
        self.column = 1
        self.dir = "down"
        self.trail = []
        self.pen = "up"
        self.append_position_to_trail()

    def configure(self, row, column, direction, pen = None):
        """Configure attributes"""
        self.row = row
        self.column = column
        self.dir = direction
        self.trail.clear()
        self.append_position_to_trail()
        if pen is not None:
            self.pen = pen

    # utility
    def get_dir(self):
        """Get current direction the AryaBota robot is facing"""
        return self.dir

    def get_state(self):
        """Get current state of the AryaBota robot's position wrapped in a dictionary"""
        grid_state = GRID.get_instance().get_state()
        return {
            "row": self.row,
            "column": self.column,
            "dir": self.dir,
            "pen": self.pen,
            "coloured": grid_state["coloured"]
        }

    def get_state_for_answer(self):
        """Get current state of the AryaBota robot's position wrapped in a dictionary"""
        return {
            "position": {
                "row": self.row,
                "column": self.column
            }
        }

    def append_position_to_trail(self, row = None, column = None):
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
