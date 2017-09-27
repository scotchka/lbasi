class VM(object):
    def __init__(self, co):
        self.co = co
        self.stack = []

    def run(self):
        i = 0
        while i < len(self.co.code):
            op, arg = self.co.code[i]
            i += 1
            run_op = getattr(self, '_' + op.lower())
            run_op(arg)

    def _push(self, arg):
        self.stack.append(arg)

    def _add(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a + b)

    def _sub(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a - b)

    def _mul(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a * b)

    def _div(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a / b)

    def _print(self, arg):
        print self.stack.pop()

    def _pop(self, arg):
        self.stack.pop()
