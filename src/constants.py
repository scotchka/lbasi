import operator
from token import Token

# token types

INTEGER = 'INTEGER'
REAL = 'REAL'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
INTEGER_DIV = 'INTEGER_DIV'
FLOAT_DIV = 'FLOAT_DIV'
EOF = 'EOF'
LPARENS = 'LPARENS'
RPARENS = 'RPARENS'
BEGIN = 'BEGIN'
END = 'END'
SEMI = 'SEMI'
DOT = 'DOT'
ID = 'ID'
ASSIGN = 'ASSIGN'
COLON = 'COLON'
COMMA = 'COMMA'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST = 'REAL_CONST'

OPS = {
    PLUS: operator.add,
    MINUS: operator.sub,
    MULTIPLY: operator.mul,
    INTEGER_DIV: operator.floordiv,
    FLOAT_DIV: operator.truediv
}

SYMBOLS = {
    '+': PLUS,
    '-': MINUS,
    '*': MULTIPLY,
    '/': FLOAT_DIV,
    '(': LPARENS,
    ')': RPARENS
}

RESERVED_KEYWORDS = {
    'BEGIN',
    'END',
    'DIV',
    'PROGRAM',
    'VAR'
}
