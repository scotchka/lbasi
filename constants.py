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
