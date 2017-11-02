class Parse(object):
    def __init__(self):
        self.string = ''
        self.pos = 0

    def consume(self, char):
        if self.pos < len(self.string) and self.string[self.pos] == char:
            self.pos += 1
            return True
        return False

    def whitespace(self):
        while self.pos < len(self.string) and self.string[self.pos].isspace():
            self.pos += 1
        return True

    def NUM(self):

        result = ''
        while self.pos < len(self.string) and self.string[self.pos].isdigit():
            result += self.string[self.pos]
            self.pos += 1

        return int(result) if result else False

    def ELEM(self):
        start = self.pos
        result = self.LIST()
        if result is not False:
            return result
        self.pos = start
        result = self.NUM()
        if result is not False:
            return result
        self.pos = start
        return False

    def ELEMS(self):
        start = self.pos
        result = (self.ELEM() is not False
                  and self.whitespace()
                  and self.consume(',')
                  and self.whitespace()
                  and self.ELEMS() is not False  # recurse
                  )
        if result is True:
            self.pos = start
            elem = self.ELEM()
            self.whitespace()
            self.consume(',')
            self.whitespace()
            elems = self.ELEMS()
            return [elem] + elems

        self.pos = start
        result = self.ELEM() is not False and self.whitespace()
        if result is True:
            self.pos = start
            elem = self.ELEM()
            self.whitespace()
            return [elem]

        self.pos = start
        return False

    def LIST(self):
        #         print 'string', self.string[self.pos:]
        start = self.pos
        result = (self.whitespace()
                  and self.consume('[')
                  and self.whitespace()
                  and self.ELEMS()
                  and self.whitespace()
                  and self.consume(']')
                  and self.whitespace()
                  )
        if result is True:
            self.pos = start
            self.whitespace()
            self.consume('[')
            self.whitespace()
            elems = self.ELEMS()
            self.whitespace()
            self.consume(']')
            self.whitespace()
            #             print 'elems', elems
            return elems

        self.pos = start
        result = (self.whitespace()
                  and self.consume('[')
                  and self.whitespace()
                  and self.consume(']')
                  and self.whitespace()
                  )

        if result is True:
            self.pos = start
            self.whitespace()
            self.consume('[')
            self.whitespace()
            self.consume(']')
            self.whitespace()
            #             print '[]', []
            return []

        self.pos = start
        #         print 'False', False
        return False

    def __call__(self, string):
        self.string = string
        self.pos = 0
        lst = self.LIST()
        if self.pos == len(self.string):
            return lst
        else:
            return False


parse = Parse()
