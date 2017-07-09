# token types

INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
EOF = 'EOF'


class Token(object):
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
        # print type_, value

    def __repr__(self):
        return '< Token {type_}: {value} >'.format(type_=self.type, value=self.value)


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    @staticmethod
    def error():
        raise Exception('Error parsing input')

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

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):

        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat(INTEGER)

        while self.current_token.type != EOF:

            op = self.current_token

            if op.type == PLUS:
                self.eat(PLUS)
            elif op.type == MINUS:
                self.eat(MINUS)
            elif op.type == MULTIPLY:
                self.eat(MULTIPLY)
            elif op.type == DIVIDE:
                self.eat(DIVIDE)
            else:
                self.error()

            right = self.current_token
            self.eat(INTEGER)

            if op.type == PLUS:
                res = left.value + right.value
            elif op.type == MINUS:
                res = left.value - right.value
            elif op.type == MULTIPLY:
                res = left.value * right.value
            else:
                res = left.value / right.value

            left = Token(INTEGER, res)

        return left.value


if __name__ == '__main__':
    while True:
        try:
            input_text = raw_input('calc> ')
        except EOFError:
            break

        if not input_text:
            continue

        interpreter = Interpreter(input_text)
        result = interpreter.expr()
        print result
