from .errors import InterpreterError
from .constants import OPS, PLUS, MINUS, MULTIPLY, INTEGER_DIV, FLOAT_DIV

from .node_visitor import NodeVisitor


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.GLOBAL_SCOPE = {}

    def visit_BinOp(self, node):
        if node.op.type in (PLUS, MINUS, MULTIPLY, INTEGER_DIV, FLOAT_DIV):
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

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        name = node.left.value
        self.GLOBAL_SCOPE[name] = self.visit(node.right)

    def visit_Var(self, node):
        name = node.value
        value = self.GLOBAL_SCOPE[name]
        return value

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)

        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        pass

    def visit_Type(self, node):
        pass

    def visit_ProcedureDecl(self, node):
        pass

    def interpret(self):
        return self.visit(self.tree)
