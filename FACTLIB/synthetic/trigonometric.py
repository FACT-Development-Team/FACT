
from synthetic.generate import Generator
from synthetic.compound import Add, Sub, Mult, Pow
from synthetic.number import Const, NConst, Var
import math

"""
This file implements nodes to generate trigonometric functions. Currently only sine and cosine are supported and they can be evaluated only at
positions that return integer numbers (e.g. cos(k*pi/2)).
"""
class Sin():
    terminals = []
    non_terminals = []
    # terminals = [Var(), Const()]
    # non_terminals = [Add(), Sub(), Mult(), NConst(positive=True)]
    def __init__(self, arg1=None):
        self.arg1 = arg1

    def finish(self, generator):
        self.arg1 = generator.generate(terminals=Sin.terminals, non_terminals=Sin.non_terminals, current=self.arg1)

    def get_options(self):
        options = 0
        if self.arg1 == None:
            options += 1
        return options

    def is_non_terminal(self):
        return True

    def evaluate(self, value):
        a = abs(self.arg1.evaluate(value)) % 4
        if a == 2:
            a = 0
        if a == 3:
            a = -1
        return a

    def to_string(self):
        return 'math.sin(math.pi/2 * (' + self.arg1.to_string() + '))'

    def get_length(self):
        return self.arg1.get_length() + 3


class Cos():
    terminals = []
    non_terminals = []
    # terminals = [Var(), Const()]
    # non_terminals = [Add(), Sub(), Mult(), NConst(positive=True)]
    def __init__(self, arg1=None):
        self.arg1 = arg1

    def finish(self, generator):
        self.arg1 = generator.generate(terminals=Cos.terminals, non_terminals=Cos.non_terminals, current=self.arg1)

    def get_options(self):
        options = 0
        if self.arg1 == None:
            options += 1
        return options

    def is_non_terminal(self):
        return True

    def evaluate(self, value):
        a = abs(self.arg1.evaluate(value)) % 4
        if a == 0:
            a = 1
        elif a == 1:
            a == 0
        elif a == 2:
            a == -1
        else:
            a == 0
        return a #int(math.cos(math.pi/2 * self.arg1.evaluate(value)))

    def to_string(self):
        return 'math.cos(math.pi/2 * (' + self.arg1.to_string() + '))'

    def get_length(self):
        return self.arg1.get_length() + 3
