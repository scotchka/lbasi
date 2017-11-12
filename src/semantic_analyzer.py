from node_visitor import NodeVisitor
from symbol import ScopedSymbolTable, VarSymbol, ProcedureSymbol


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        builtins_scope = ScopedSymbolTable(scope_name='builtins', scope_level=0)
        builtins_scope._init_builtins()
        self.current_scope = builtins_scope

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Program(self, node):
        builtins_scope = self.current_scope
        builtins_scope.insert(ProcedureSymbol(node.name))
        print builtins_scope

        print 'ENTER scope: global'
        global_scope = ScopedSymbolTable(scope_name='global', scope_level=1, enclosing_scope=self.current_scope)
        self.current_scope.global_scope = global_scope
        self.current_scope = global_scope
        self.visit(node.block)

        print global_scope

        self.current_scope = self.current_scope.enclosing_scope

        print 'LEAVE scope: global'
        return builtins_scope

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
        type_symbol = self.current_scope.lookup(type_name)

        var_name = node.var_node.value

        var_symbol = VarSymbol(var_name, type_symbol)
        self.current_scope.insert(var_symbol)

    def visit_Assign(self, node):
        self.visit(node.right)
        self.visit(node.left)

    def visit_Var(self, node):
        var_name = node.value
        self.current_scope.lookup(var_name)

    def visit_ProcedureDecl(self, node):
        proc_name = node.proc_name
        proc_symbol = ProcedureSymbol(proc_name)
        self.current_scope.insert(proc_symbol)

        print 'ENTER scope: %s' % proc_name
        procedure_scope = ScopedSymbolTable(
            scope_name=proc_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        setattr(self.current_scope, proc_name+'_scope', procedure_scope)
        self.current_scope = procedure_scope

        for param in node.params:
            param_type = self.current_scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = VarSymbol(param_name, param_type)
            self.current_scope.insert(var_symbol)
            proc_symbol.params.append(var_symbol)

        self.visit(node.block_node)

        print procedure_scope

        self.current_scope = self.current_scope.enclosing_scope

        print 'LEAVE scope: %s' % proc_name
