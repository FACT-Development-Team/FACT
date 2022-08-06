
import copy
from random import randrange, choices, randint

class Generator():
    def __init__(self, length=None):
        self.options = 1
        self.length = generate_coinflips() if length is None else length

    def generate(self, terminals, non_terminals, current=None):
        #print("CUrrent length ", str(self.length), " and options, ", str(self.options))
        if current == None:  
            current = self.get_item(terminals, non_terminals)
        self.options += current.get_options() - 1 #if current.is_non_terminal() else 0
        self.options = max(self.options, 1)
        self.length -= 1 if current.is_non_terminal() else 0
        current.finish(self)
        return current

    def get_item(self, terminals, non_terminals):
        coin = biased_coin(1/self.options) and self.length > 0
        if (terminals is None or coin) and non_terminals is not None:
            library = non_terminals
        else:
            library = terminals

        next = randrange(len(library))
        item = copy.deepcopy(library[next])
        return item

    def get_length(self):
        return self.length

def generate_coinflips():
    coin = randint(0, 1)
    return 1 + generate_coinflips() if coin else 0

def biased_coin(p):
    return 0 if p == 0 else choices([0, 1], weights=(1 - p, p), k=1)[0]

