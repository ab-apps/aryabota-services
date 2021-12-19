"""Importing Grid Module"""
from singleton_classes import Grid
from singleton_classes import AryaBota

class DictCompareWrapper:
    """Comparing dictionaries"""
    def __init__(self, json):
        self.json = json
    def __eq__(self, other):
        comp = True
        obj = self.json
        other_obj = other.json
        for key in obj.keys():
            if comp:
                if key not in other_obj.keys():
                    return False
                comp = comp and obj[key] == other_obj[key]
            else:
                return False
        return comp

class ListCompareWrapper:
    """Comparing lists"""
    def __init__(self, array, compare_type):
        self.array = array
        self.compare_type = compare_type
    def __eq__(self, other):
        if self.compare_type == "lenient":
            comp = True
            for item in self.array:
                if comp:
                    comp = comp and item in other.array
                else:
                    return False
            return comp
        elif self.compare_type == "strict":
            if len(self.array) != len(other.array):
                return False
            comp = True
            for item in self.array:
                comp = comp and item in other.array
                if comp:
                    index_self = self.array.index(item)
                    index_other = other.array.index(item)
                    self.array.pop(index_self)
                    other.array.pop(index_other)
                else:
                    return False
            return comp
        else:
            return self.array == other.array

def wrap(obj, compare_type):
    """Wrappers"""
    if isinstance(obj, dict):
        for key in obj.keys():
            obj[key] = wrap(obj[key], compare_type)
        obj = DictCompareWrapper(obj)
    elif isinstance(obj, list):
        for i in range(len(obj)): #pylint: disable=consider-using-enumerate
            obj[i] = wrap(obj[i], compare_type)
        obj = ListCompareWrapper(obj, compare_type)
    return obj

class Problem:
    """ the Singleton Problem, its attributes and state"""
    __instance = None
    @staticmethod
    def get_instance():
        """Static access method"""
        if Problem.__instance is None:
            Problem()
        return Problem.__instance

    def __init__(self):
        """Virtually private constructor"""
        # TODO This class gets initialised twice, check why? On hot reload it happens only once, but on starting server
        # it happens twice
        if Problem.__instance is not None:
            raise Exception("This class is a singleton!")
        Problem.__instance = self
        self.type = self.statement = ""
        self.answer = []
        self.custom_answer = ""

    def get_type(self):
        """return problem type"""
        return self.type

    def configure(self, problem_type, statement, answer, answer_message):
        """Configure attributes"""
        self.type = problem_type
        self.statement = statement
        self.answer = answer
        self.custom_answer = answer_message

    def compare_states(self, submitted_answer):
        """Comparing states"""
        reqd_state = self.answer["state"]
        compare_type = self.answer["type"]
        reqd_ans = wrap(reqd_state, compare_type)
        ans = wrap(submitted_answer, compare_type)
        return reqd_ans == ans

    def compare_values(self, submitted_answer):
        """Comparing values"""
        if self.answer["value_type"] != "string":
            return self.answer["value"] == submitted_answer
        else:
            if not isinstance(submitted_answer, str):
                return False
            return self.answer["value"].lower() == submitted_answer.lower()

    def check_answer(self, submitted_answer):
        """Checking answer"""
        succeeded = None
        message = "Not implemented yet!"
        if self.type == "value_match":
            succeeded = self.compare_values(submitted_answer)
        elif self.type == "state_match":
            succeeded = self.compare_states(submitted_answer)
        if succeeded:
            message = 'Correct answer!'
            if self.custom_answer['message']:
                message = self.custom_answer['message']
        else:
            message = 'Wrong answer, please try again'
        return {
            "succeeded": succeeded,
            "message": message
        }

    def get_initial_state(self):
        """Return intial state of problem"""
        grid = Grid.get_instance()
        bot = AryaBota.get_instance()
        grid_state = grid.get_state()
        arya_bota_state = bot.get_state()
        grid_state.update(arya_bota_state)
        grid_state["type"] = self.type
        if self.type == "state_match":
            if "arya_bota" in self.answer["state"]:
                grid_state["homes"] = [self.answer["state"]["arya_bota"]]
        return grid_state
