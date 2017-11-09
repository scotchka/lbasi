from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.semantic_analyzer import SemanticAnalyzer

if __name__ == '__main__':
    import sys

    with open(sys.argv[1]) as f:
        text = f.read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symtab_builder = SemanticAnalyzer()
    symtab_builder.visit(tree)
    print
    print 'Symbol Table contents:'
    print symtab_builder.scope

    interpreter = Interpreter(tree)
    result = interpreter.interpret()

    print
    print 'Runtime GLOBAL_MEMORY contents:'
    for k, v in sorted(interpreter.GLOBAL_SCOPE.items()):
        print '%s = %s' % (k, v)
