from synthetic.generate import Generator
from random import randrange
import sys

class Periodic():
    """
    Periodic is a non_terminal that is used to generate periodic functions. The way how this is done is by creating an expression and specifyin periodicity,
    in which case the experession is repeated after periodicty ends.
    """
    terminals = []
    non_terminals = []

    def __init__(self, arg1=None, periodicity=None):
        self.arg1 = arg1
        self.periodicity = randrange(1,250) if periodicity is None else periodicity

    def finish(self, generator):
        self.arg1 = generator.generate(terminals=Periodic.terminals, non_terminals=Periodic.non_terminals, current=self.arg1)

    def get_options(self):
        options = 0
        if self.arg1 == None:
            options += 1
        return options

    def is_non_terminal(self):
        return True

    def evaluate(self, value):
        return self.arg1.evaluate(value%self.periodicity)

    def to_string(self):
        return 'periodic(' + self.arg1.to_string() + ', ' + str(self.periodicity) + ')'

    def get_length(self):
        return self.arg1.get_length() + 3 + len(str(self.periodicity))
