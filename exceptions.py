class CompilerError(Exception):
    pass


class ParserError(CompilerError):
    pass


class LexerError(CompilerError):
    pass


class InterpreterError(CompilerError):
    pass
