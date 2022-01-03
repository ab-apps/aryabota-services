import ply.lex as lex
import logging

class LexerError(Exception): pass

tokens = [
    'MOVE',
    'TURNLEFT',
    'TURNRIGHT',
    'PENUP',
    'PENDOWN',
    'SUBMIT',
    'PRINT',
    'NEWLINE',
    'REPEAT',
    'OTHERS'
]

#t_ignore = ' '

def t_MOVE(t):
    r'move[ ]*[0-9]+'
    steps = t.value.split('move')[-1]
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

def t_SUBMIT(t):
    r'submit[ ]*.*'
    value = ''.join(t.value.split('submit')).strip()
    t.value = "submit({value})".format(value=value)
    return t

def t_PRINT(t):
    r'print[ ]*.*'
    value = ''.join(t.value.split('print')).strip()
    t.value = "print({value})".format(value=value)
    return t

def t_REPEAT(t):
    r'repeat[ ]*.*'
    substr1 = "repeat"
    substr2 = "times"
    index1 = t.value.index(substr1)
    index2 = t.value.index(substr2)
    times = ""
    for i in range(index1 + len(substr1), index2):
        times = times + t.value[i]
    t.value = "for i in range({value}):".format(value=int(times))
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

stage2_lexer = lex.lex()