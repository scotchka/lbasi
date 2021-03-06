from collections import OrderedDict
from .errors import UndeclaredVariable, DuplicateDeclaration


class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class BuiltinTypeSymbol(Symbol):
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__, name=self.name
        )

    def __eq__(self, other):
        return self.name == other.name


class VarSymbol(Symbol):
    def __repr__(self):
        return "<{class_name}(name='{name}', type='{type}')>".format(
            class_name=self.__class__.__name__, name=self.name, type=self.type
        )

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type


class ProcedureSymbol(Symbol):
    def __init__(self, name, params=None):
        super(ProcedureSymbol, self).__init__(name)
        if params is None:
            params = []

        self.params = params

    def __repr__(self):
        return "<{class_name}(name={name}, parameters={params})>".format(
            class_name=self.__class__.__name__, name=self.name, params=self.params,
        )

    def __eq__(self, other):
        return self.name == other.name


class ScopedSymbolTable(object):
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self._symbols = OrderedDict()
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope

    def _init_builtins(self):
        self.insert(BuiltinTypeSymbol("INTEGER"))
        self.insert(BuiltinTypeSymbol("REAL"))

    def __repr__(self):
        h1 = "SCOPE (SCOPED SYMBOL TABLE)"
        lines = ["\n", h1, "=" * len(h1)]
        for header_name, header_value in (
            ("Scope name", self.scope_name),
            ("Scope level", self.scope_level),
            (
                "Enclosing scope",
                self.enclosing_scope.scope_name if self.enclosing_scope else None,
            ),
        ):
            lines.append("%-15s: %s" % (header_name, header_value))
        h2 = "Scope (Scoped symbol table) contents"
        lines.extend([h2, "-" * len(h2)])
        lines.extend(("%7s: %r" % (key, value)) for key, value in self._symbols.items())
        lines.append("\n")
        s = "\n".join(lines)
        return s

    def insert(self, symbol):
        print("Insert: %s" % symbol.name)
        if symbol.name in self._symbols:
            raise DuplicateDeclaration(repr(symbol.name))
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        print("Lookup: %s. (Scope name: %s)" % (name, self.scope_name))
        symbol = self._symbols.get(name)

        if symbol is not None:
            return symbol

        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)

        raise UndeclaredVariable(repr(name))
