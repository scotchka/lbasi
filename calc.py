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
        raise Exception('Invalid character')

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


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    @staticmethod
    def error():
        raise Exception('Invalid syntax')

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
            return token.value
        elif token.type == LPARENS:
            self.eat(LPARENS)
            result = self.expr()
            self.eat(RPARENS)
            return result
        else:
            self.error()

    def term(self):

        result = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE):
            op = self.current_token
            self.eat(op.type)
            right = self.factor()
            result = OPS[op.type](result, right)

        return result


    def expr(self):
        """
        expr: TERM ((PLUS|MINUS)TERM)*

        """

        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token

            self.eat(op.type)

            right = self.term()

            result = OPS[op.type](result, right)

        return result


if __name__ == '__main__':
    while True:
        try:
            text = raw_input('calc> ')
        except EOFError:
            break

        if not text:
            continue
        lexer = Lexer(text)

        try:
            interpreter = Interpreter(lexer)
        except Exception as e:
            print 'Invalid expression'
            continue

        result = interpreter.expr()
        print result
