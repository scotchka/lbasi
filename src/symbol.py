from collections import OrderedDict

class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinTypeSymbol, self).__init__(name)

    def __repr__(self):
        return self.name


class VarSymbol(Symbol):
    def __init__(self, name, type):
        super(VarSymbol, self).__init__(name, type)

    def __repr__(self):
        return '<{name}: {type}>'.format(name=self.name, type=self.type)


class SymbolTable(object):
    def __init__(self):
        self._symbols = OrderedDict()
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol('INTEGER'))
        self.define(BuiltinTypeSymbol('REAL'))

    def __repr__(self):
        return 'Symbols: {symbols}'.format(
            symbols=[val for val in self._symbols.values()]
        )

    def define(self, symbol):
        print 'Define: %s' % symbol
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        print 'Lookup: %s' % name
        return self._symbols.get(name)

