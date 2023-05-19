import ply.lex as lex
import builtins

forbidden_names = dir(builtins)

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
    'ASSIGN',
    "FPYINIT",
    "FPYCLOSE"
]

reserved = {
    'True': 'BOOLEAN',
    'False': 'BOOLEAN',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'deff': 'DEFF',
    'case': 'CASE'
}

tokens += list(set(reserved.values()))


def t_FPYINIT(t):
    r'"""FPY'
    return t


def t_FPYCLOSE(t):
    r'"""'
    t.lexer.lineno+=1
    return t


def t_PERIOD(t):
    r'\.'
    return t


def t_COLON(t):
    r':'
    return t


def t_SEMICOLON(t):
    r';'
    return t


def t_CONCAT(t):
    r'\+\+'
    return t


def t_PLUS(t):
    r'\+'
    return t


def t_MINUS(t):
    r'-'
    return t


def t_MULT(t):
    r'\*'
    return t


def t_FLOORDIV(t):
    r'//'
    return t


def t_DIV(t):
    r'/'
    return t


def t_MOD(t):
    r'%'
    return t


def t_POWER(t):
    r'\^'
    return t


def t_LPAREN(t):
    r'\('
    return t


def t_RPAREN(t):
    r'\)'
    return t


def t_LSQUARE(t):
    r'\['
    return t


def t_RSQUARE(t):
    r'\]'
    return t


def t_LBRACE(t):
    r'\{'
    return t


def t_RBRACE(t):
    r'\}'
    return t


def t_COMMA(t):
    r','
    return t


def t_LE(t):
    r'<='
    return t


def t_LT(t):
    r'<'
    return t


def t_GE(t):
    r'>='
    return t


def t_GT(t):
    r'>'
    return t


def t_EQ(t):
    r'=='
    return t


def t_NE(t):
    r'!='
    return t


def t_ASSIGN(t):
    r'='
    return t


def t_AND(t):
    r'&&'
    return t


def t_OR(t):
    r'\|\|'
    return t


def t_NOT(t):
    r'!'
    return t


def t_FLOAT(t):
    r'\d+\.\d+'
    return t


def t_INTEGER(t):
    r'\d+'
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    elif t.value in forbidden_names:
        line = t.lexer.lineno
        col = find_column(t.lexer.lexdata, t)
        raise Exception(f"{line}:{col}: <lexer error> Reserved python token '{t.value}'")
    else:
        t.type = 'IDENTIFIER'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



t_ignore = ' \t'


def t_error(t):
    line = t.lexer.lineno
    col = find_column(t.lexer.lexdata, t)
    raise Exception(f"{line}:{col}: <lexer error> Illegal character '{t.value[0]}'")


def find_column(input, token=None, lexpos=None):
    if token is not None:
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return token.lexpos - line_start + 1
    elif lexpos is not None:
        line_start = input.rfind('\n', 0, lexpos) + 1
        return lexpos - line_start + 1
    else:
        raise ValueError("Either token or lexpos must be provided")



lexer = lex.lex()
