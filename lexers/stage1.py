import ply.lex as lex
import logging

class LexerError(Exception): pass

tokens = [
    'MYROW',
    'MYCOLUMN',
    'NUMBER_OF_COINS',
    'ASSIGN',
    'OBSTACLEAHEAD',
    'OBSTACLEBEHIND',
    'OBSTACLELEFT',
    'OBSTACLERIGHT',
    'COMMENT',
    'NEWLINE',
    'OTHERS'
]

#t_ignore = ' '

def t_COMMENT(t):
    r'\#(.)*\n'
    pass

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

stage1_lexer = lex.lex()