from errors import ParserError
from constants import INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, LPARENS, RPARENS


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
