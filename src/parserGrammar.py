import ply.yacc as yacc
import lexer

tokens = lexer.tokens

start = 'program'



def p_program(p):
    """
    program : function_declarations
    """

def p_function_declarations(p):
    """ 
    function_declarations : function_declaration
                          | function_declaration function_declarations
    """

def p_function_declaration(p):
    """ 
    function_declaration : DEFF IDENTIFIER COLON LBRACE function_body RBRACE
    """

def p_function_body(p):
    """ 
    function_body : case_statement SEMICOLON
                  | case_statement SEMICOLON function_body
    """

def p_case_statement(p):
    """ 
    case_statement : CASE case_input ASSIGN statement
    """

def p_case_input(p):
    """ 
    case_input : LPAREN RPAREN
               | LPAREN function_arguments RPAREN
    """
    
def p_statement(p):
    """ 
    statement : IF bool THEN statement ELSE statement
              | bool
    """

def p_list(p):
    """
    list : LSQUARE RSQUARE
         | LSQUARE list_elements RSQUARE
    """
    
    
def p_list_elements(p):
    """ 
    list_elements : bool
                  | bool COMMA list_elements
    """
    
def p_bool(p):
    """ 
    bool : bool OR join 
         | join
    """

def p_join(p):
    """ 
    join : join AND equality
         | equality
    """
    
def p_equality(p):
    """ 
    equality : equality EQ rel 
             | equality NE rel
             | rel
    """
    
def p_rel(p):
    """
    rel : listop LT listop 
        | listop GT listop
        | listop LE listop
        | listop GE listop
        | listop
    """

def p_listop(p):
    """
    listop : expr COLON listop
           | expr CONCAT listop
           | expr
    """
def p_expr(p):
    """ 
    expr : expr PLUS term
         | expr MINUS term
         | term
    """

def p_term(p):
    """ 
    term : term MULT exponential
         | term DIV exponential
         | term FLOORDIV exponential 
         | term MOD exponential
         | exponential
    """
    
def p_exponential(p):
    """ 
    exponential : exponential POWER unary
                | unary
    """
    
def p_unary(p):
    """ 
    unary : NOT unary 
          | MINUS unary 
          | PLUS unary
          | factor
    """

def p_factor(p):
    """
    factor : LPAREN bool RPAREN
           | ID
           | function_call
           | INT
           | FLO
           | BOOL
           | list 
    """

def p_INT(p):
    """ 
    INT : INTEGER
    """
    p[0] = "int"

def p_FLO(p):
    """ 
    FLO : FLOAT
    """
    p[0] = "float"
    
def p_BOOL(p):
    """ 
    BOOL : BOOLEAN
    """
    p[0] = "boolean"
    
def p_ID(p):
    """ 
    ID : IDENTIFIER
    """
    p[0] = "any"
    
def p_function_composition(p):
    """ 
    function_composition : IDENTIFIER
                         | IDENTIFIER PERIOD function_composition
    """
    
def p_function_call(p):
    """ 
    function_call : function_composition LPAREN function_arguments RPAREN
                  | function_composition LPAREN RPAREN 
    """
    p[0] = "any"
    
def p_function_arguments(p):
    """ 
    function_arguments : bool
                       | bool COMMA function_arguments
    """

def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}'")
    else:
        print("Syntax error: Unexpected end of input")


parser = yacc.yacc()

input_string = """
deff sum:
{
    case ([]) = 0;
    case ((x:xs)) = x + sum(xs); 
}

deff soma_impares:
{
    case ([]) = 0;
    case ((x:xs)) = if ! x % 2 == 0 then soma_impares(xs) else x + soma_impares(xs);
}

deff filtra_impares:
{
    case ([]) = [];
    case ((x:xs)) = if ! x % 2 == 0 then filtra_impares(xs) else x ++ filtra_impares(xs);
}

deff soma_impares_2:{
    case(x) = sum . filtra_impares(x);
}

deff mult:
{
    case (a,b) = a*b;
}

deff id:
{
    case (a) = a;
}

deff func_const:
{
    case() = 3;
}

deff mult_list_Num:
{
    case ([],i) = [];
    case ((x:xs),i) = i*x : mult_list_Num(xs,i);
}

deff nzp:
{
    case (a) = if a > 0 then 1 else if a == 0 then 0 else -1;
}

deff fib:
{
    case (soma(1)) = 0;
    case (!True || 2^5>4) = i*x : mult_list_Num(i);
    case (2*4) = fib(n-1) + fib(n-2);
}

deff maximo:
{
    case([x]) = x;
    case(x:xs) = max (x,(maximo (xs)));
}

deff ord:
{
    case([])=True;
    case([x])=True;
    case(x:y:xs) = x <= y && ord(y:xs);
}

deff concatena:
{
    case([],ys) = ys;
    case((x:xs),ys) = x : concatena(xs,ys);
}

deff soma_impares_2:
{
    case(x) = sum . filtra_impares(x) : [1,2,3] ;
}
"""

result = parser.parse(input_string)
print("Done")

"""while input_string:
    input_string = input(">> ")
    result = parser.parse(input_string)"""
