from exceptions import InterpreterError
from constants import OPS, PLUS, MINUS, MULTIPLY, DIVIDE


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
