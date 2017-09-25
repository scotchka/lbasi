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


class CompilerError(Exception):
    pass


class ParserError(CompilerError):
    pass


class LexerError(CompilerError):
    pass


class InterpreterError(CompilerError):
    pass


#
# Lexer
#


class Token(object):
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
        # print type_, value

    def __repr__(self):
        return '< Token {type_}: {value} >'.format(type_=self.type, value=self.value)


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    @staticmethod
    def error():
        raise LexerError('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        digits = []
        while self.current_char is not None and self.current_char.isdigit():
            digits.append(self.current_char)
            self.advance()
        return int(''.join(digits))

    def get_next_token(self):

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char in SYMBOLS:
                current_char = self.current_char
                self.advance()
                return Token(SYMBOLS[current_char], current_char)

            self.error()

        return Token(EOF, None)


#
# Parser
#

class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self):
        return 'BinOp({left}, {token}, {right})'.format(left=repr(self.left),
                                                        token=repr(self.token.value),
                                                        right=repr(self.right))


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return 'Num({})'.format(self.value)


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    @staticmethod
    def error():
        raise ParserError('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        factor: INTEGER

        """
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPARENS:
            self.eat(LPARENS)
            node = self.expr()
            self.eat(RPARENS)
            return node
        elif token.type in (PLUS, MINUS):
            self.eat(token.type)
            return UnaryOp(token, self.factor())
        else:
            self.error()

    def term(self):

        node = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        expr: TERM ((PLUS|MINUS)TERM)*

        """

        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token

            self.eat(token.type)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        return self.expr()


#
# Interpreter
#

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise InterpreterError('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type in (PLUS, MINUS, MULTIPLY, DIVIDE):
            return OPS[node.op.type](self.visit(node.left), self.visit(node.right))
        else:
            raise InterpreterError('unknown binary operation')

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        if node.op.type == MINUS:
            return -self.visit(node.expr)
        elif node.op.type == PLUS:
            return +self.visit(node.expr)
        else:
            raise InterpreterError('unknown unary operation')

    def interpret(self):
        ast = self.parser.parse()
        return self.visit(ast)


if __name__ == '__main__':
    while True:
        try:
            text = raw_input('calc> ')
        except EOFError:
            break

        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)

        try:
            result = interpreter.interpret()
        except CompilerError as e:
            print 'Invalid expression'
            continue
        else:
            print result
