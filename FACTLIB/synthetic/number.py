
from synthetic.generate import Generator
from random import randrange, choices, randint
"""
It contains the nodes for numbers: Var(), Const() and NConst().
We distinguish between Const() and NConst(). With Const() numbers 0,1,2,3,4,5,6,7,8,9 can be generated. NConst() is a non_terminal that is used to generate sequences with higher length.
"""
class Var():
    """
    Var() is a terminal that is used for variable (typically denoted 'x').
    """
    def finish(self, generator):
        pass

    def get_options(self):
        options = 0
        return options

    def is_non_terminal(self):
        return False

    def evaluate(self, value):
        return value

    def to_string(self):
        return 'x'

    def get_length(self):
        return 1


class Const():
    """
    Terminal used to generate numbers from {0,1,2,3,4,5,6,7,8,9}. Can be conditioned to positive in which case 0 is excluded.
    The reason for having the option to choose only from {1,2,3,...,9} (without 0), is for NConst() which makes possible to avoid numbers like 0000123.
    """
    def __init__(self, positive=False, arg1=None):
        self.arg1 = arg1
        self.positive = positive

    def finish(self, generator):
        if self.arg1 == None:
            if self.positive:
                self.arg1 = randrange(1,10)
            else:
                self.arg1 = randrange(0,10)

    def get_options(self):
        options = 0
        return options

    def is_non_terminal(self):
        return False

    def evaluate(self, value):
        return self.arg1

    def to_string(self):
        return str(self.arg1)

    def get_length(self):
        return 1

class NConst():
    """
    NConst() is a non_terminal that is used to generate numbers with any length.
    """
    def __init__(self, positive=False, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.positive = positive

    def finish(self, generator):
        self.arg1 = generator.generate(terminals=[Const(positive=self.positive)], non_terminals=None, current=self.arg1)
        self.arg2 = generator.generate(terminals=[Const()], non_terminals=[NConst()], current=self.arg2)

    def get_options(self):
        options = 0
        if self.arg2 == None:
            options += 1
        return options

    def is_non_terminal(self):
        return True

    def evaluate(self, value):
        return int(str(self.arg1.evaluate(value)) + str(self.arg2.evaluate(value)))

    def to_string(self):
        return self.arg1.to_string() + self.arg2.to_string()

    def get_length(self):
        return self.arg1.get_length() + self.arg2.get_length()
