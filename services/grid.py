""" the Singleton Grid, its attributes and state"""
class Grid:
    """Properties:
        rows: number of rows, default 10
        columns: number of columns, default 10
        many moreeee"""
    __instance = None
    @staticmethod
    def get_instance():
        """Static access method"""
        if Grid.__instance is None:
            Grid()
        return Grid.__instance

    def __init__(self):
        """Virtually private constructor"""
        # TODO This class gets initialised twice, check why? On hot reload it happens only once, but on starting server
        # it happens twice
        if Grid.__instance is not None:
            raise Exception("This class is a singleton!")
        Grid.__instance = self
        self.rows = 1
        self.columns = 1
        self.homes = self.coins = self.coloured = self.coins_per_position = self.obstacles = self.obstacles_per_position = []
        self.statement = self.problem_spec = ""

    def configure(self, rows, columns, coins = None, coins_per_position = None, obstacles = None, obstacles_per_position = None, homes = None, statement = None, problem_spec = None):
        """Configure attributes"""
        self.rows = rows
        self.columns = columns
        self.homes = []
        zero_coins = [[0 for i in range(rows)] for j in range(columns)]
        self.coins = self.coins_per_position = self.obstacles = self.obstacles_per_position = zero_coins
        self.coloured = []
        self.statement = statement
        self.problem_spec = problem_spec
        if coins is not None:
            self.coins = coins
        if coins_per_position is not None:
            self.coins_per_position = coins_per_position
        if obstacles is not None:
            self.obstacles = obstacles
        if obstacles_per_position is not None:
            self.obstacles_per_position = obstacles_per_position
        if homes is not None:
            self.homes = homes

    def colour(self, pos):
        """Colouring the trail as required"""
        if pos not in self.coloured:
            self.coloured.append(pos)

    def get_number_of_coins(self, row, column):
        """Get number of coins at a given position in the grid, ie, (row, column)"""
        if self.coins_per_position is not None:
            if row <= self.rows and column <= self.columns:
                return self.coins_per_position[row - 1][column - 1]
            raise Exception("This position does not exist on the grid!")
        # TODO decide whether to just return 0 instead?
        raise Exception("No coins are present in this grid!")

    def get_state(self):
        """get current state"""
        if self.__instance:
            return {
                "rows": self.rows,
                "columns": self.columns,
                "coins": self.coins,
                "coins_per_position": self.coins_per_position,
                "obstacles": self.obstacles,
                "obstacles_per_position": self.obstacles_per_position,
                "homes": self.homes,
                "statement": self.statement,
                "problem_spec": self.problem_spec
            }
        return {}

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
