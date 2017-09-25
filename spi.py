from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from exceptions import CompilerError

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
