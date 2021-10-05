import ply.lex as lex
import ply.yacc as yacc
import logging

from services.utils import convert_english_pseudocode_to_python
from control_hub import *
from services.grid import Grid
from services.coin_sweeper import CoinSweeper

bot = CoinSweeper.get_instance()
grid = Grid.get_instance()
excep = ""

class LexerError(Exception): pass

tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'MODULO',
    'MYROW',
    'MYCOLUMN',
    'MOVE',
    'TURNLEFT',
    'TURNRIGHT',
    'PENUP',
    'PENDOWN',
    'NUMBER_OF_COINS',
    'REPEAT',
    'TIMES',
    'IDENTIFIER',
    'ASSIGN',
    'IF',
    'ELSE',
    'OBSTACLEAHEAD',
    'OBSTACLEBEHIND',
    'OBSTACLELEFT',
    'OBSTACLERIGHT',
    'PRINT',
    'SUBMIT',
    'BEGIN',
    'END',
    'LT',
    'GT',
    'LTE',
    'GTE',
    'EQUALS',
    'NOTEQUALS',
    'PYTHON',
    'COMMENT',
]

t_ignore = ' \t'

def t_COMMENT(t):
    r'\#(.)*\n'
    pass

def t_PYTHON(t):
    r'python[ ]*begin(.|\n)*python[ ]*end'
    t.type = 'PYTHON'
    return t

def t_PLUS(t):
    r'\+'
    t.value = 'PLUS'
    return t

def t_MINUS(t):
    r'\-'
    t.value = 'MINUS'
    return t

def t_MULTIPLY(t):
    r'\*'
    t.value = 'MULTIPLY'
    return t

def t_DIVIDE(t):
    r'\/'
    t.value = 'DIVIDE'
    return t

def t_MODULO(t):
    r'%'
    t.value = 'MODULO'
    return t

def t_COMMA(t):
    r'\,'
    t.value = 'COMMA'
    return t

def t_MOVE(t):
    r'move'
    t.value = 'MOVE'
    return t

def t_TURNLEFT(t):
    r'turn[ ]*left'
    t.value = 'TURNLEFT'
    return t

def t_TURNRIGHT(t):
    r'turn[ ]*right'
    t.value = 'TURNRIGHT'
    return t

def t_PENUP(t):
    r'pen[ ]*up'
    t.value = 'PENUP'
    return t

def t_PENDOWN(t):
    r'pen[ ]*down'
    t.value = 'PENDOWN'
    return t  

def t_MYROW(t):
    r'my[ ]*row'
    t.value = "MYROW"
    return t

def t_MYCOLUMN(t):
    r'my[ ]*column'
    t.value = "MYCOLUMN"
    return t

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    t.type = 'NUMBER'
    return t

def t_BEGIN(t):
    r'begin'
    t.value = 'BEGIN'
    return t

def t_END(t):
    r'end'
    t.value = 'END'
    return t

def t_IF(t):
    r'if'
    t.value = 'IF'
    return t

def t_ELSE(t):
    r'else'
    t.value = 'ELSE'
    return t

def t_OBSTACLEAHEAD(t):
    r'obstacle[ ]*ahead'
    t.value = 'OBSTACLEAHEAD'
    return t

def t_OBSTACLEBEHIND(t):
    r'obstacle[ ]*behind'
    t.value = 'OBSTACLEBEHIND'
    return t

def t_OBSTACLELEFT(t):
    r'obstacle[ ]*left'
    t.value = 'OBSTACLELEFT'
    return t

def t_OBSTACLERIGHT(t):
    r'obstacle[ ]*right'
    t.value = 'OBSTACLERIGHT'
    return t

def t_NUMBER_OF_COINS(t):
    r'number[ ]*of[ ]*coins'
    t.value = 'NUMBER_OF_COINS'
    return t

def t_PRINT(t):
    r'print'
    t.value = 'PRINT'
    return t

def t_SUBMIT(t):
    r'submit'
    t.value = 'SUBMIT'
    return t

def t_REPEAT(t):
    r'repeat'
    t.value = 'REPEAT'
    return t

def t_TIMES(t):
    r'times'
    t.value = 'TIMES'
    return t

def t_LTE(t):
    r'is[ ]*lesser[ ]*than[ ]*or[ ]*equal[ ]*to'
    t.value = 'LTE'
    return t

def t_GTE(t):
    r'is[ ]*greater[ ]*than[ ]*or[ ]*equal[ ]*to'
    t.value = 'GTE'
    return t

def t_LT(t):
    r'is[ ]*lesser[ ]*than'
    t.value = 'LT'
    return t

def t_GT(t):
    r'is[ ]*greater[ ]*than'
    t.value = 'GT'
    return t

def t_EQUALS(t):
    r'equals'
    t.value = 'EQUALS'
    return t

def t_NOTEQUALS(t):
    r'not equals'
    t.value = 'NOTEQUALS'
    return t

def t_ASSIGN(t):
    r'is'
    t.value = 'ASSIGN'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-z_][a-zA-Z0-9]*'
    t.type = 'IDENTIFIER'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    """Error in lexing token"""
    logging.error(f'Invalid token: {t.value[0]}')
    t.lexer.skip(1)

english_lexer = lex.lex()

def p_commands(p):
    '''
    expr : expr expr
    '''
    p[0] = p[1] + "\n" + p[2]
    global excep
    if len(excep)>0:
        p[0] = excep
        excep = ""

def p_command(p):
    '''
    expr : TURNLEFT
        | TURNRIGHT
        | PENUP
        | PENDOWN
        | MOVE NUMBER
        | assign_expr
        | selection_expr
        | repeat_expr
        | print_expr
        | submit_expr
        | PYTHON
    '''
    if p[1] in ['TURNLEFT', 'TURNRIGHT', 'PENUP', 'PENDOWN']:
        python_code = convert_english_pseudocode_to_python(p[1])
        p[0] = python_code
    elif len(p) == 2:
        try:
            program = p[1]
            program = program.replace('python begin\n','')
            program = program.replace('python end','')
            p[0] = program
        except:
            p[0] = p[1]
    elif len(p) == 3:
        python_code = convert_english_pseudocode_to_python(p[1], steps = p[2])
        p[0] = python_code
    global excep
    p[0] = excep

def p_print_expr(p):
    '''
    print_expr : PRINT value_expr
    '''
    python_code = convert_english_pseudocode_to_python("PRINT_VALUE", expr = p[2])
    p[0] = python_code

def p_value_expr(p):
    '''
    value_expr : value_expr operator value_expr
                | operand
    '''
    if len(p) == 4:
        var1 = p[1]
        var2 = p[3]
        python_code = convert_english_pseudocode_to_python(p[2], variable1 = var1, variable2 = var2)
    else:
        python_code = p[1]
    p[0] = python_code

def p_operand(p):
    '''
    operand :   MYROW
               | MYCOLUMN
               | IDENTIFIER
               | NUMBER
               | NUMBER_OF_COINS
               | OBSTACLEAHEAD
               | OBSTACLERIGHT
               | OBSTACLEBEHIND
               | OBSTACLELEFT
    '''
    if (p[1] in ['MYROW', 'MYCOLUMN', 'OBSTACLEAHEAD', 'OBSTACLERIGHT', 'OBSTACLEBEHIND', 'OBSTACLELEFT']):
        python_code = convert_english_pseudocode_to_python(p[1])
    elif p[1] == 'IDENTIFIER':
        python_code = convert_english_pseudocode_to_python("IDENTIFIER", variable = p[1])
    elif p[1] == 'NUMBER_OF_COINS':
        python_code = convert_english_pseudocode_to_python("GET_COINS")
    else: # case NUMBER
        python_code = convert_english_pseudocode_to_python("NUMBER", value = p[1])
    p[0] = python_code

def p_operator(p):
    '''
    operator :   PLUS
               | MINUS
               | MULTIPLY
               | DIVIDE
               | MODULO
               | LT
               | GT
               | LTE
               | GTE
               | EQUALS
               | NOTEQUALS
    '''
    p[0] = p[1]

def p_selection_expr(p):
    '''
    selection_expr : IF value_expr BEGIN expr END ELSE BEGIN expr END
                    | IF value_expr BEGIN expr END
    '''
    if len(p) == 6:
        p[4] = '\n\t' + p[4].replace('\n', '\n\t')
        python_code = convert_english_pseudocode_to_python(p[1], expr = p[2])
        p[0] = python_code + " " + p[4]
    else:
        p[4] = '\n\t' + p[4].replace('\n', '\n\t')
        p[8] = '\n\t' + p[8].replace('\n', '\n\t')
        python_code_if = convert_english_pseudocode_to_python(p[1], expr = p[2])
        python_code_else = convert_english_pseudocode_to_python(p[6])
        p[0] = python_code_if + " " + p[4] + "\n" + python_code_else + " " + p[8]

def p_repeat_expr(p):
    '''
    repeat_expr : REPEAT NUMBER TIMES BEGIN expr END
    '''
    p[5] = '\n\t' + p[5].replace('\n', '\n\t')
    python_code = convert_english_pseudocode_to_python(p[1], times = p[2])
    p[0] = python_code + " " + p[5]

def p_assign_expr(p):
    '''
    assign_expr : IDENTIFIER ASSIGN value_expr
    '''
    python_code = convert_english_pseudocode_to_python("ASSIGNMENT", variable = p[1], expr = p[3])
    p[0] = python_code

def p_submit_expr(p):
    '''
    submit_expr : SUBMIT
                | SUBMIT value_expr
    '''
    if len(p) == 3:
        python_code = convert_english_pseudocode_to_python("SUBMIT", value = p[2])
    elif len(p) == 2:
        python_code = convert_english_pseudocode_to_python("SUBMIT", value = '')
    p[0] = python_code
    
def p_error(p):
    """Error in parsing command"""
    global excep
    excep = "Aryabota doesn't recognize '{word}'".format(word = str(p.value))
    logging.error("p_error")
    logging.error(excep)
    logging.error(f'Syntax error in input: {str(p.value)}')

english_parser = yacc.yacc()