from synthetic.generate import Generator
from random import randrange

class Finite():
    """
    Finite is a nonterminal that has one possible production rules (any expression) and it has a value between 1 and 500 which defines the end of the sequence.
    The expression can be terminals or non_terminals. Those are chosen, based on the given sets defined for Mult.
    """
    terminals = []
    non_terminals = []

    def __init__(self, arg1=None, final=None):
        self.arg1 = arg1
        self.final = randrange(1,500) if final is None else final

    def finish(self, generator):
        self.arg1 = generator.generate(terminals=Finite.terminals, non_terminals=Finite.non_terminals, current=self.arg1)

    def get_options(self):
        options = 0
        if self.arg1 == None:
            options += 1
        return options

    def is_non_terminal(self):
        return True

    def evaluate(self, value):
        if value > self.final or value < 0:
            return "UNDEFINED"
        return self.arg1.evaluate(value)

    def to_string(self):
        return 'finite(' + self.arg1.to_string() + ', ' + str(self.final) + ')'

    def get_length(self):
        return self.arg1.get_length() + 3 + len(str(self.final))
