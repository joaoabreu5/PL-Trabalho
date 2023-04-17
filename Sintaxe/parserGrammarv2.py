import ply.yacc as yacc
import lexerv2

tokens = lexerv2.tokens

start = 'program'

def p_function_type(p):
    """ 
    function_type : T_INT
                  | T_FLOAT
                  | T_BOOLEAN
                  | T_LIST LSQUARE function_type RSQUARE
    """

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
    function_declaration : DEFF IDENTIFIER function_input ARROW function_output LBRACE function_body RBRACE
    """

def p_function_input(p):
    """
    function_input : LPAREN RPAREN 
                   | LPAREN function_input_arguments RPAREN
    """

def p_function_input_arguments(p):
    """ 
    function_input_arguments : function_type 
                             | function_type COMMA function_input_arguments
    """
    
def p_function_output(p):
    """
    function_output : function_type
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
           | IDENTIFIER
           | function_call
           | INTEGER
           | FLOAT
           | BOOLEAN
           | list 
    """


def p_function_composition(p):
    """ 
    function_composition : IDENTIFIER
                         | IDENTIFIER PERIOD IDENTIFIER
    """
    
def p_function_call(p):
    """ 
    function_call : function_composition LPAREN function_arguments RPAREN
                  | function_composition LPAREN RPAREN 
    """
    
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

input_string = """deff sum(list[int]) -> int
{
    case ([]) = 0;
    case ((x:xs)) = x + sum(xs); 
}

deff soma_impares(list[int]) -> int
{
    case ([]) = 0;
    case ((x:xs)) = if ! x % 2 == 0 then soma_impares(xs) else x + soma_impares(xs);
}

deff filtra_impares(list[int]) -> list[int]
{
    case ([]) = [];
    case ((x:xs)) = if ! x % 2 == 0 then filtra_impares(xs) else x ++ filtra_impares(xs);
}

deff soma_impares_2(list[int]) -> int {
    case(x) = sum . filtra_impares(x);
}

deff mult(float,float)->float
{
    case (a,b) = a*b;
}

deff id(float)->float
{
    case (a) = a;
}

deff func_const()->float 
{
    case() = 3;
}

deff mult_list_Num(list[int], int) -> list[int]
{
    case ([],i) = [];
    case ((x:xs),i) = i*x : mult_list_Num(xs,i);
}

deff nzp(int) -> int
{
    case (a) = if a > 0 then 1 else if a == 0 then 0 else -1;
}

deff fib(int) -> int
{
    case (soma(1)) = 0;
    case (!True || 2^5>4) = i*x : mult_list_Num(i);
    case (2*4) = fib(n-1) + fib(n-2);
}

deff maximo(list[float])->float
{
    case([x]) = x;
    case(x:xs) = max (x,(maximo (xs)));
}

deff ord(list[int])->boolean
{
    case([])=True;
    case([x])=True;
    case(x:y:xs) = x <= y && ord(y:xs);
}

deff concatena(list[int],list[int])->list[int]
{
    case([],ys) = ys;
    case((x:xs),ys) = x : concatena(xs,ys);
}

deff soma_impares_2(list[int]) -> int {
    case(x) = sum . filtra_impares(x) : [1,2,3] ;
}
"""

result = parser.parse(input_string)
print("Done")

"""while input_string:
    input_string = input(">> ")
    result = parser.parse(input_string)"""
    
