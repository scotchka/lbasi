from .errors import ParserError
from .constants import (
    INTEGER_CONST,
    PLUS,
    MINUS,
    MULTIPLY,
    INTEGER_DIV,
    LPARENS,
    RPARENS,
    DOT,
    BEGIN,
    END,
    SEMI,
    ID,
    ASSIGN,
    EOF,
    REAL_CONST,
    VAR,
    COMMA,
    COLON,
    REAL,
    INTEGER,
    PROGRAM,
    FLOAT_DIV,
    PROCEDURE,
)

from .ast import (
    Num,
    UnaryOp,
    BinOp,
    Block,
    Assign,
    Program,
    Compound,
    Type,
    VarDecl,
    Var,
    NoOp,
    ProcedureDecl,
    Param,
)


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    @staticmethod
    def error():
        raise ParserError("Invalid syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        factor: PLUS factor
              | MINUS factor
              | INTEGER_CONST
              | REAL_CONST
              | LPARENS expr RPARENS
              | variable

        """
        token = self.current_token
        if token.type in {INTEGER_CONST, REAL_CONST}:
            self.eat(token.type)
            return Num(token)
        elif token.type == LPARENS:
            self.eat(LPARENS)
            node = self.expr()
            self.eat(RPARENS)
            return node
        elif token.type in (PLUS, MINUS):
            self.eat(token.type)
            return UnaryOp(token, self.factor())
        else:
            return self.variable()

    def term(self):

        node = self.factor()

        while self.current_token.type in (MULTIPLY, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        expr: TERM ((PLUS|MINUS)TERM)*

        """

        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token

            self.eat(token.type)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def program(self):
        """
        program: PROGRAM variable SEMI block DOT
        """
        self.eat(PROGRAM)
        var_node = self.variable()
        name = var_node.value
        self.eat(SEMI)
        block = self.block()
        self.eat(DOT)
        return Program(name, block)

    def block(self):
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        return Block(declaration_nodes, compound_statement_node)

    def declarations(self):
        """declarations : (VAR (variable_declaration SEMI)+)*
                        | (PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI)*
                        | empty
        """
        declarations = []

        while True:
            if self.current_token.type == VAR:
                self.eat(VAR)
                while self.current_token.type == ID:
                    var_decl = self.variable_declaration()
                    declarations.extend(var_decl)
                    self.eat(SEMI)

            elif self.current_token.type == PROCEDURE:
                self.eat(PROCEDURE)
                proc_name = self.current_token.value
                self.eat(ID)
                params = []

                if self.current_token.type == LPARENS:
                    self.eat(LPARENS)
                    params.extend(self.formal_parameter_list())
                    self.eat(RPARENS)

                self.eat(SEMI)
                block_node = self.block()
                declarations.append(ProcedureDecl(proc_name, params, block_node))
                self.eat(SEMI)

            else:
                break

        return declarations

    def formal_parameter_list(self):
        """ formal_parameter_list : formal_parameters
                                  | formal_parameters SEMI formal_parameter_list
        """
        if self.current_token.type != ID:
            return []

        param_nodes = self.formal_parameters()

        while self.current_token == SEMI:
            self.eat(SEMI)
            param_nodes.extend(self.formal_parameters())

        return param_nodes

    def formal_parameters(self):
        """ formal_parameters : ID (COMMA ID)* COLON type_spec """
        var_nodes = [self.variable()]

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(self.variable())

        self.eat(COLON)

        type_node = self.type_spec()

        return [Param(var_node, type_node) for var_node in var_nodes]

    def variable_declaration(self):
        var_nodes = [self.variable()]

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(self.variable())

        self.eat(COLON)

        type_node = self.type_spec()
        return [VarDecl(var_node, type_node) for var_node in var_nodes]

    def type_spec(self):
        token = self.current_token

        if token.type == INTEGER:
            self.eat(INTEGER)
        else:
            self.eat(REAL)

        return Type(token)

    def compound_statement(self):
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = Compound()
        root.children.extend(nodes)

        return root

    def statement_list(self):
        nodes = [self.statement()]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            nodes.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return nodes

    def statement(self):
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()

        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        return NoOp()

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node
