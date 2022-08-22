from synthetic.generate import Generator
import sys

class Modulo():
    """
    Modulo is a tuple of two nonterminals (exp1 % exp2).
    The expression can be terminals or non_terminals. Those are chosen, based on the given sets defined for Modulo.
    Special case is modulo 0. In this case we define exp % 0 = 0.
    """

    terminals = []
    non_terminals = []

    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2

    def finish(self, generator):
        self.arg1 = generator.generate(terminals=Modulo.terminals, non_terminals=Modulo.non_terminals, current=self.arg1)
        self.arg2 = generator.generate(terminals=Modulo.terminals, non_terminals=Modulo.non_terminals, current=self.arg2)

    def get_options(self):
        options = 0
        if self.arg1 == None:
            options += 1
        return options

    def is_non_terminal(self):
        return True

    def evaluate(self, value):
        m = self.arg2.evaluate(value)
        if m == 0:
            return 0
        else:
            return self.arg1.evaluate(value) % m

    def to_string(self):
        return 'mod(' + self.arg1.to_string() + ',' + self.arg2.to_string() + ')'

    def get_length(self):
        return self.arg1.get_length() + self.arg2.get_length() + 1
