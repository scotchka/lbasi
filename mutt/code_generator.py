class Code(object):
    def __init__(self):
        self.code = []
        self.names = []
        self.consts = []
        self.globals = {}


class CodeGenerator(object):
    def __call__(self, tree):
        self.co = Code()
        self.visit(tree)
        return self.co

    def _visit_children(self, node):
        for child in node.children:
            self.visit(child)

    def visit(self, node):
        node_class = type(node).__name__

        if node_class == 'Tree':
            node_type = node.data
        elif node_class == 'Token':
            node_type = node.type

        visit_method = getattr(self, 'visit_' + node_type)
        visit_method(node)

    def visit_add(self, node):
        left, right = node.children
        self.visit(left)
        self.visit(right)
        self.co.code.append(('ADD', None))

    def visit_sub(self, node):
        left, right = node.children
        self.visit(left)
        self.visit(right)
        self.co.code.append(('SUB', None))

    def visit_mul(self, node):
        left, right = node.children
        self.visit(left)
        self.visit(right)
        self.co.code.append(('MUL', None))

    def visit_div(self, node):
        left, right = node.children
        self.visit(left)
        self.visit(right)
        self.co.code.append(('DIV', None))

    def visit_print(self, node):
        self._visit_children(node)
        self.co.code.append(('PRINT', None))

    def visit_stmt(self, node):
        self._visit_children(node)
        self.co.code.append(('POP', None))

    def visit_block(self, node):
        self._visit_children(node)

    def visit_NUMBER(self, node):
        self.co.code.append(('PUSH', int(node.value)))
