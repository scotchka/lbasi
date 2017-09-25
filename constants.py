import operator

# token types

INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
EOF = 'EOF'
LPARENS = 'LPARENS'
RPARENS = 'RPARENS'
BEGIN = 'BEGIN'
END = 'END'
SEMI = 'SEMI'
DOT = 'DOT'
ID = 'ID'
ASSIGN = 'ASSIGN'


OPS = {
    PLUS: operator.add,
    MINUS: operator.sub,
    MULTIPLY: operator.mul,
    DIVIDE: operator.div
}

SYMBOLS = {
    '+': PLUS,
    '-': MINUS,
    '*': MULTIPLY,
    '/': DIVIDE,
    '(': LPARENS,
    ')': RPARENS
}

RESERVED_KEYWORDS = {
    'BEGIN',
    'END'
}