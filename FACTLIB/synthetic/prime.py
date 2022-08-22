# Prime number generator

def prime_generator():
    n = 2
    while True:     # n starts from 2 to end
        for x in range(2, n):   # check if x can be divided by n
            if n % x == 0:      # if true then n is not prime
                break
        else:                   # if x is found after exhausting all values of x
            yield n             # generate the prime
        n = n + 1

g = prime_generator()
primes = [next(g) for i in range(1000)]

from synthetic.generate import Generator
import sys

class Prime():
    """
    Prime is a non_terminal used to generate prime related sequences. The way how this is done, is we generate sequences by giving inductive bias
    in using prime numbers. Instead of using number k, sequences can also use prime(k) which returns the k'th prime number from {2,3,5, ....}.
    """
    terminals = []
    non_terminals = []

    def __init__(self, arg1=None):
        self.arg1 = arg1

    def finish(self, generator):
        self.arg1 = generator.generate(terminals=Prime.terminals, non_terminals=Prime.non_terminals, current=self.arg1)

    def get_options(self):
        options = 0
        if self.arg1 == None:
            options += 1
        return options

    def is_non_terminal(self):
        return True

    def evaluate(self, value):
        return primes[self.arg1.evaluate(value)]

    def to_string(self):
        return 'primes(' + self.arg1.to_string() + ')'

    def get_length(self):
        return self.arg1.get_length() + 5
