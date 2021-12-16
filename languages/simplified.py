import ply.lex as lex
import logging

from services.utils import convert_english_pseudocode_to_python
from control_hub import *
from services.grid import Grid
from services.coin_sweeper import CoinSweeper

bot = CoinSweeper.get_instance()
grid = Grid.get_instance()

class LexerError(Exception): pass

tokens = [
    'MYROW',
    'MYCOLUMN',
    'MOVE',
    'TURNLEFT',
    'TURNRIGHT',
    'PENUP',
    'PENDOWN',
    'NUMBER_OF_COINS',
    'ASSIGN',
    'OBSTACLEAHEAD',
    'OBSTACLEBEHIND',
    'OBSTACLELEFT',
    'OBSTACLERIGHT',
    'SUBMIT',
    'PRINT',
    'COMMENT',
    'NEWLINE',
    'OTHERS'
]

t_ignore = ' '

def t_COMMENT(t):
    r'\#(.)*\n'
    pass

def t_MOVE(t):
    r'move[ ]*[0-9]+'
    steps = t.value.split(' ')[-1]
    t.value = "move({steps})".format(steps=steps)
    return t

def t_TURNLEFT(t):
    r'turn[ ]*left'
    t.value = "turn()"
    return t

def t_TURNRIGHT(t):
    r'turn[ ]*right'
    t.value = "turn('right')"
    return t

def t_PENUP(t):
    r'pen[ ]*up'
    t.value = "set_pen('up')"
    return t

def t_PENDOWN(t):
    r'pen[ ]*down'
    t.value = "set_pen('down')"
    return t  

def t_MYROW(t):
    r'my[ ]*row'
    t.value = "get_my_row()"
    return t

def t_MYCOLUMN(t):
    r'my[ ]*column'
    t.value = "get_my_column()"
    return t

def t_OBSTACLEAHEAD(t):
    r'obstacle[ ]*ahead'
    t.value = "obstacle_ahead()"
    return t

def t_OBSTACLEBEHIND(t):
    r'obstacle[ ]*behind'
    t.value = "obstacle_behind()"
    return t

def t_OBSTACLELEFT(t):
    r'obstacle[ ]*left'
    t.value = "obstacle_left()"
    return t

def t_OBSTACLERIGHT(t):
    r'obstacle[ ]*right'
    t.value = "obstacle_right()"
    return t

def t_NUMBER_OF_COINS(t):
    r'number[ ]*of[ ]*coins'
    t.value = "get_number_of_coins()"
    return t

def t_SUBMIT(t):
    r'submit[ ]*.*'
    value = ''.join(t.value.split('submit')).strip()
    t.value = "submit({value})".format(value=value)
    return t

def t_PRINT(t):
    r'print[ ]*.*'
    value = ''.join(t.value.split('print')).strip()
    t.value = "print_value({value})".format(value=value)
    return t

def t_ASSIGN(t):
    r' is '
    t.value = "="
    return t

def t_NEWLINE(t):
    r'\n+'
    t.value = "\n"
    return t

def t_OTHERS(t):
    r'.'
    t.type = 'OTHERS'
    return t

def t_error(t):
    """Error in lexing token"""
    logging.error(f'Invalid token: {t.value[0]}')
    t.lexer.skip(1)

simplified_lexer = lex.lex()