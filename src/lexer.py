import ply.lex as lex

tokens = [
    'INTEGER',
    'FLOAT',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'FLOORDIV',
    'MOD',
    'POWER',
    'LPAREN',
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'COLON',
    'CONCAT',
    'LE',
    'LT',
    'GE',
    'GT',
    'EQ',
    'NE',
    'IDENTIFIER',
    'AND',
    'OR',
    'NOT',
    'PERIOD',
    'SEMICOLON',
    'ASSIGN'
]

reserved = {
    'True': 'BOOLEAN',
    'False': 'BOOLEAN',
    'if' : 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'deff' : 'DEFF',
    'case': 'CASE'
}

tokens += list(set(reserved.values()))

t_PERIOD = r'\.'
t_COLON = r':'
t_SEMICOLON = r';'
t_CONCAT = r'\+\+'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_FLOORDIV = r'//'
t_DIV = r'/'
t_MOD = r'%'
t_POWER = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_LE = r'<='
t_LT = r'<'
t_GE = r'>='
t_GT = r'>'
t_EQ = r'=='
t_NE = r'!='
t_ASSIGN = r'='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir o analisador léxico
lexer = lex.lex()
