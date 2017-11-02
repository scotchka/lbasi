from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.errors import CompilerError

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as f:
        text = f.read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print interpreter.GLOBAL_SCOPE
