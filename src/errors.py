class CompilerError(Exception):
    pass


class ParserError(CompilerError):
    pass


class LexerError(CompilerError):
    pass


class InterpreterError(CompilerError):
    pass


class SemanticError(Exception):
    pass


class UndeclaredVariable(SemanticError):
    pass


class DuplicateDeclaration(SemanticError):
    pass
