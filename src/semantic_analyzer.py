from node_visitor import NodeVisitor
from symbol import ScopedSymbolTable, VarSymbol
from errors import UndeclaredVariable, DuplicateDeclaration


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.scope = ScopedSymbolTable(scope_name='global', scope_level=1)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Num(self, node):
        pass

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_VarDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.scope.lookup(type_name)

        var_name = node.var_node.value
        if self.scope.lookup(var_name) is not None:
            raise DuplicateDeclaration(repr(var_name))

        var_symbol = VarSymbol(var_name, type_symbol)
        self.scope.insert(var_symbol)

    def visit_Assign(self, node):
        self.visit(node.right)
        self.visit(node.left)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.scope.lookup(var_name)
        if var_symbol is None:
            raise UndeclaredVariable(repr(var_name))

    def visit_ProcedureDecl(self, node):
        pass
