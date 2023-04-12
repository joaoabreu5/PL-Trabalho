import ply.yacc as yacc
import my_lexer

tokens = my_lexer.tokens

start = 'expr'

def p_expr(p):
    """ 
    expr : exprBoolean
        | exprNum
        | exprList
    """
    p[0] = p[1]
 
def p_num_constant(p):
    """
    num_constant : DOUBLE 
                 | INT
    """
    p[0] = p[1]

def p_constant(p):
    """ 
    constant : num_constant
             | BOOLEAN
    """
    p[0] = p[1]
    
def p_list(p):
    """
    list : LBRACKET RBRACKET 
         | LBRACKET list_elements RBRACKET 
    """
    if len(p) == 3:
        p[0] = []  
    else:
        p[0] = p[2]  

    
def p_list_elements(p):
    """ 
    list_elements : list_element
                  | list_element COMMA list_elements
    """
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_list_element(p):
    """ 
    list_element  : expr
    """
    p[0] = p[1] 
    
def p_exprNum(p):
    """
    exprNum : termNum 
            | exprNum OP_SUMSUB termNum

    """
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        if p[3] == 'INT' :
            p[0] = p[1] - int(p[3])
        elif p[3] == 'DOUBLE' :
            p[0] = p[1] - float(p[3])
        else:
            p[0] = p[1] - p[3]
    else:
        p[0] = None

def p_termNum(p):
    """
    termNum : OP_SUMSUB termNum
            | factorNum
            | termNum OP_MULTDIV factorNum
    """
    if p[1] == '-':
        p[0] = -p[2]
    elif p[1] == '+':
        p[0] = p[2]
    elif len(p) == 2:
        p[0] = p[1]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]
    else:
        p[0] = p[1] // p[3]

def p_factorNum(p):
    """
    factorNum : LPAREN exprNum RPAREN
              | num_constant
    """
    if (len(p) > 2):
        p[0] = p[2]
    else:
        p[0] = p[1]
 
def p_exprBoolean(p):
    """ 
    exprBoolean : factorBoolean
                | exprBoolean OP_LOGIC factorBoolean
                | exprBoolean OP_COMPARATOR factorBoolean
    """
    
    if (len(p) == 2):
        p[0] = p[1]
    else:
        if p[2] == '&&':
            p[0] = p[1] and p[3]
        elif p[2] == '||':
            p[0] = p[1] or p[3]
        elif p[2] == '<':
            p[0] = p[1] < p[3]
        elif p[2] == '>':
            p[0] = p[1] > p[3]
        elif p[2] == '>=':
            p[0] = p[1] >= p[3]
        elif p[2] == '<=':
            p[0] = p[1] <= p[3]
        elif p[2] == '==':
            p[0] = p[1] == p[3]
        else:
            p[0] = p[1] != p[3]
        
def p_factorBoolean(p):
    """
    factorBoolean : LPAREN exprBoolean RPAREN
                  | BOOLEAN
                  | NOT factorBoolean
                  | exprComparator
                
    """
    if (len(p) == 2):
        if(p[1] == 'true'):
            p[0] = True
        elif(p[1] == 'false'):
            p[0] = False
        else:
            p[0] = p[1]
    elif p[1] == '!':
        p[0] = not p[2]
    else:
        p[0] = p[2]
        

def p_exprComparator(p):
    """ 
    exprComparator : exprNum OP_COMPARATOR exprNum 
                   | exprList OP_COMPARATOR exprList
    """
    if p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    else:
        p[0] = p[1] != p[3]


def p_exprList(p):
    """ 
    exprList : list
             | constant COLON exprList 
             | exprList COLON exprList
             | exprList DOUBLEPLUS exprList
    """
    if (len(p) == 2):
        p[0] = p[1]
    elif p[2] == ':':
        p[0] = [p[1]] + p[3]
    else:
        p[0] = p[1] + p[3]


parser = yacc.yacc(debug=True, write_tables=True)

input_string = "a"

while input_string:
    input_string = input(">> ")
    result = parser.parse(input_string)
    print(result)


