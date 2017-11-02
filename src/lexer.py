from errors import LexerError
from constants import (SYMBOLS, EOF, RESERVED_KEYWORDS, ID, ASSIGN, SEMI, DOT, INTEGER_DIV,
                       INTEGER_CONST, REAL_CONST, COLON, COMMA, FLOAT_DIV)

from token import Token


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

    def skip_comment(self):
        while self.current_char != '}':
            self.advance()
        self.advance()

    def number(self):
        digits = []
        while self.current_char is not None and self.current_char.isdigit():
            digits.append(self.current_char)
            self.advance()

        if self.current_char == '.':
            digits.append(self.current_char)
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                digits.append(self.current_char)
                self.advance()

            return Token(REAL_CONST, float(''.join(digits)))

        return Token(INTEGER_CONST, int(''.join(digits)))

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        result = result.upper()

        if result in RESERVED_KEYWORDS:
            return RESERVED_KEYWORDS[result]

        return Token(ID, result)

    def get_next_token(self):

        while self.current_char is not None:
            # print 'current char:', self.current_char

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char in SYMBOLS:
                current_char = self.current_char
                self.advance()
                return Token(SYMBOLS[current_char], current_char)

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == '/':
                self.advance()
                return Token(FLOAT_DIV, '/')

            self.error()

        return Token(EOF, None)

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        return self.text[peek_pos]
