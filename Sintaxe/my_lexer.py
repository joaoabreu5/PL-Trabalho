import ply.lex as lex

# definir a lista de tokens
tokens = ['INT', 'DOUBLE', 'BOOLEAN', 'ID', 'OP_SUMSUB', 'OP_MULTDIV', 'OP_LOGIC', 'OP_COMPARATOR', 'EQUAL', 'NOT',
          'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COLON', 'COMMA', 'SEMICOLON', 'IF', 'THEN', 'ELSE', 'ELIF', 
          'DEFF', 'CASE', 'RETURN', 'LIST', 'DOT','DOUBLEPLUS' ,'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULUS', 'FLOORDIV',
          'ARROW', 'TYPE']


# expressões regulares para cada token

t_DOUBLEPLUS = r'\+\+'
t_OP_SUMSUB = r'[+-]'
t_OP_MULTDIV = r'//|[*/%]'
t_OP_LOGIC = r'&&|\|\|'
t_OP_COMPARATOR = r'[<>]=?|==|!='
t_EQUAL = r'='
t_NOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COLON = r':'
t_COMMA = r','
t_SEMICOLON = r';'
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_ELIF = r'elif'
t_DEFF = r'deff'
t_CASE = r'case'
t_RETURN = r'return'
t_LIST = r'List'
t_DOT = r'\.'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULUS = r'%'
t_FLOORDIV = r'//'
t_ARROW = r'->'
t_TYPE = 'int|double|boolean'

# expressões regulares com ações associadas
def t_DOUBLE(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

def t_ID(t):
    r'[a-z]\w*'
    return t

# Ignorar espaços em branco e tabs
t_ignore = ' \t'

# Definir o número de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Lidar com erros de caractere inválido
def t_error(t):
    print(f"Caractere inválido '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir o analisador léxico
lexer = lex.lex()