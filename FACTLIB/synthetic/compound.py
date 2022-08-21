from synthetic.generate import Generator
from synthetic.number import Var
import sys

class Add():
    terminals = []
    non_terminals = []

    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2

    def finish(self, generator):
        self.arg1 = generator.generate(terminals=Add.terminals, non_terminals=Add.non_terminals, current=self.arg1)
        self.arg2 = generator.generate(terminals=Add.terminals, non_terminals=Add.non_terminals, current=self.arg2)

    def get_options(self):
        options = 0
        if self.arg1 == None:
            options += 1
        if self.arg2 == None:
            options += 1
        return options

    def set_terminals(terminals):
        Add.terminals = terminals

    def set_non_terminals(non_terminals):
        Add.non_terminals = non_terminals

    def is_non_terminal(self):
        return True

    def evaluate(self, value):
        return self.arg1.evaluate(value) + self.arg2.evaluate(value)

    def to_string(self):
        return '(' + self.arg1.to_string() + ' + ' + self.arg2.to_string() + ')'

    def get_length(self):
        return self.arg1.get_length() + self.arg2.get_length() + 1


class Sub():
    terminals = []
    non_terminals = []

    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2

    def finish(self, generator):
        self.arg1 = generator.generate(terminals=Sub.terminals, non_terminals=Sub.non_terminals, current=self.arg1)
        self.arg2 = generator.generate(terminals=Sub.terminals, non_terminals=Sub.non_terminals, current=self.arg2)

    def get_options(self):
        options = 0
        if self.arg1 == None:
            options += 1
        if self.arg2 == None:
            options += 1
        return options

    def set_terminals(terminals):
        Sub.terminals = terminals

    def set_non_terminals(non_terminals):
        Sub.non_terminals = non_terminals

    def is_non_terminal(self):
        return True

    def evaluate(self, value):
        return (self.arg1.evaluate(value)) - (self.arg2.evaluate(value))

    def to_string(self):
        left = "("
        right = ""
        left += self.arg1.to_string()
        right += ' - (' + self.arg2.to_string() + '))'
        return left + right

    def get_length(self):
        return self.arg1.get_length() + self.arg2.get_length() + 1

class Mult():
    terminals = []
    non_terminals = []

    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2

    def finish(self, generator):
        self.arg1 = generator.generate(terminals=Mult.terminals, non_terminals=Mult.non_terminals, current=self.arg1)
        self.arg2 = generator.generate(terminals=Mult.terminals, non_terminals=Mult.non_terminals, current=self.arg2)

    def get_options(self):
        options = 0
        if self.arg1 == None:
            options += 1
        if self.arg2 == None:
            options += 1
        return options

    def is_non_terminal(self):
        return True

    def evaluate(self, value):
        return self.arg1.evaluate(value) * self.arg2.evaluate(value)

    def to_string(self):
        left = "("
        right = ""

        if isinstance(self.arg1, Add) or isinstance(self.arg1, Sub):
            left += '(' + self.arg1.to_string() + ')'
        else:
            left += self.arg1.to_string()

        if isinstance(self.arg2, Add) or isinstance(self.arg2, Sub):
            right += ' * ' + '(' + self.arg2.to_string() + ')'
        else:
            right += ' * ' + self.arg2.to_string()
        return left + right + ')'

    def get_length(self):
        return self.arg1.get_length() + self.arg2.get_length() + 1

class Pow():
    terminals_base = []
    non_terminals_base = []

    terminals_exponent = []
    non_terminals_exponent = []

    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2

    def finish(self, generator):
        self.arg1 = generator.generate(terminals=Pow.terminals_base, non_terminals=Pow.non_terminals_base, current=self.arg1)
        self.arg2 = generator.generate(terminals=Pow.terminals_exponent, non_terminals=Pow.non_terminals_exponent, current=self.arg2)

    def set_parent(self, parent):
        self.parent = parent

    def get_options(self):
        options = 0
        if self.arg1 == None:
            options += 1
        if self.arg2 == None:
            options += 1
        return options

    def is_non_terminal(self):
        return True

    def evaluate(self, value):
        #if abs(self.arg1.evaluate(value)) > 1e5 or abs(self.arg2.evaluate(value)) > 1e5:
        #    return sys.maxsize
        return self.arg1.evaluate(value) ** abs(self.arg2.evaluate(value))

    def to_string(self):
        left = "("
        right = ""
        if isinstance(self.arg1, Add) or isinstance(self.arg1, Sub) or isinstance(self.arg1, Mult) or isinstance(self.arg1, Pow):
            left += '(' + self.arg1.to_string() + ')'
        else:
            left += self.arg1.to_string()
        right += '**'
        if isinstance(self.arg2, Var):
            right += '(' + self.arg2.to_string() + '))'
        else:
            right += self.arg2.to_string() + ')'
        return left + right

    def get_length(self):
        return self.arg1.get_length() + self.arg2.get_length() + 1
