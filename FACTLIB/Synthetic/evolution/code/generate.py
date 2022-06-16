import sys
import copy
import numpy as np
import time
import os
import logging
from random import randrange, choices, randint
from typing import Union

"""
N O T E S:
- Uncomment #if self.parent == None: options += 1# in all get_options functions
  when growing upwards is implemented!
"""

class Poly_builder():
    def __init__(self, length:int=None):
        self.options = 1
        self.length = generate_coinflips() if length == None else length

    def generate(self, parent=None, current=None):
        if current == None:  
            item = self.get_item()
            item.set_parent(parent)
            item.visited = True
            self.options += item.get_options() - 1
            self.length -= 1 if item.is_non_terminal() else 0
            item.finish(self)
        return item

    def generate_number(self, parent, current, is_leading:bool):
        if current == None:
            item = self.get_item_number(is_leading)
            item.set_parent(parent)
            item.visited = True
            self.options += item.get_options() - 1
            self.length -= 1 if item.is_non_terminal() else 0
            item.finish(self)
        else:
            item = current
            item.set_parent(parent)
            item.visited = True
            self.options += item.get_options() - 1
            self.length -= 1 if item.is_non_terminal() else 0
            item.finish(self)
        return item
    
    def generate_constant(self, parent, current):        
        item = current
        item.set_parent(parent)
        item.visited = True
        item.finish(self)
        return item
            
    def get_item(self):
        coin = biased_coin(1/self.options) and self.length > 0
        if coin:
            library = non_terminals
        else:
            library = terminals

        next = randrange(len(library))
        item = copy.deepcopy(library[next])
        return item

    def get_item_number(self, is_leading):
        coin = biased_coin(1/self.options) and self.length > 0
        if coin:
            item = NConst(Const2(), None) if is_leading else NConst(Const(), None)
        else:
            item = Const()
        return item

#------- CLASSES -------#

class Const():
    def __init__(self, arg1=None):
        self.arg1 = arg1
        self.parent = None

    def finish(self, poly_builder:Poly_builder):
        if self.arg1 == None:
            self.arg1 = randrange(10)

    def set_parent(self, parent):
        self.parent = parent

    def get_options(self):
        options = 0
        return options

    def is_non_terminal(self):
        return False

    def evaluate(self, value):
        return self.arg1

    def to_string(self):
        return str(self.arg1)

class Const2():
    def __init__(self, arg1=None):
        self.arg1 = arg1
        self.parent = None
        self.visited = False

    def finish(self, poly_builder:Poly_builder):
        if self.arg1 == None:
            self.arg1 = randrange(1, 10)

    def set_parent(self, parent):
        self.parent = parent

    def get_options(self):
        options = 0
        return options

    def is_non_terminal(self):
        return False

    def evaluate(self, value):
        return self.arg1

    def to_string(self):
        return str(self.arg1)

class NConst():
    def __init__(self, arg1:Union[Const, Const2]=None, arg2:Union[Const, Const2, 'NConst']=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.parent = None

    def finish(self, poly_builder:Poly_builder):
        self.arg1 = poly_builder.generate_constant(parent=self, current=self.arg1)
        self.arg2 = poly_builder.generate_number(parent=self, current=self.arg2, is_leading=False)
    
    def set_parent(self, parent):
        self.parent = parent

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

class Var():
    def __init__(self):
        self.parent = None

    def finish(self, poly_builder:Poly_builder):
        pass

    def set_parent(self,parent):
        self.parent = parent

    def get_options(self):
        options = 0
        return options

    def is_non_terminal(self):
        return False

    def evaluate(self, value):
        return value

    def to_string(self):
        return 'x'

class Add():
    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.parent = None 

    def finish(self, poly_builder:Poly_builder):
        self.arg1 = poly_builder.generate(parent=self, current=self.arg1)
        self.arg2 = poly_builder.generate(parent=self, current=self.arg2)

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
        return self.arg1.evaluate(value) + self.arg2.evaluate(value)

    def to_string(self):
        return self.arg1.to_string() + ' + ' + self.arg2.to_string()

class Sub():
    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.parent = None

    def finish(self, poly_builder:Poly_builder):
        self.arg1 = poly_builder.generate(parent=self, current=self.arg1)
        self.arg2 = poly_builder.generate(parent=self, current=self.arg2)

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
        return (self.arg1.evaluate(value)) - (self.arg2.evaluate(value))

    def to_string(self):
        left = ""
        right = ""
        left += self.arg1.to_string()

        if isinstance(self.arg2, Const) or isinstance(self.arg2, Var) or isinstance(self.arg2, Pow) or isinstance(self.arg2, NConst):
            right += ' - ' + self.arg2.to_string()
        else:
            right += ' - (' + self.arg2.to_string() + ')'
        return left + right

class Mult():
    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.parent = None

    def finish(self, poly_builder:Poly_builder):
        self.arg1 = poly_builder.generate(parent=self, current=self.arg1)
        self.arg2 = poly_builder.generate(parent=self, current=self.arg2)

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
        return self.arg1.evaluate(value) * self.arg2.evaluate(value)

    def to_string(self):
        left = ""
        right = ""
        
        if isinstance(self.arg1, Add) or isinstance(self.arg1, Sub):
            left += '(' + self.arg1.to_string() + ')'
        else:
            left += self.arg1.to_string()

        if isinstance(self.arg2, Add) or isinstance(self.arg2, Sub):
            right += ' * ' + '(' + self.arg2.to_string() + ')'
        else:
            right += ' * ' + self.arg2.to_string()
        return left + right

class Pow():
    def __init__(self, arg1=None, arg2:Union[Const, NConst]=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.parent = None

    def finish(self, poly_builder:Poly_builder):
        self.arg1 = poly_builder.generate(parent=self, current=self.arg1)
        self.arg2 = poly_builder.generate_number(parent=self, current=self.arg2, is_leading=True)

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
        if abs(self.arg1.evaluate(value)) > 1e5 or abs(self.arg2.evaluate(value)) > 1e5:
            return sys.maxsize
        return self.arg1.evaluate(value) ** self.arg2.evaluate(value)

    def to_string(self):
        left = ""
        right = ""
        if isinstance(self.arg1, Add) or isinstance(self.arg1, Sub) or isinstance(self.arg1, Mult):
            left += '(' + self.arg1.to_string() + ')'
        else:
            left += self.arg1.to_string()
        right += '^' + self.arg2.to_string()
        return left + right


#------- SET CONTEXT-FREE GRAMMAR -------#

terminals = [Var(), Const()]
non_terminals = [Add(), Sub(), Mult(), Pow(), NConst(arg1=Const2())]


#------- AUXILIARY FUNCTIONS -------#

def biased_coin(p):
    return 0 if p == 0 else choices([0, 1], weights=(1 - p, p), k=1)[0]

def generate_coinflips():
    coin = randint(0, 1)
    return 1 + generate_coinflips() if coin else 0

def mean_squared_error(y_true:list, y_pred:list) -> int:
    return abs((sum([np.square(i - j) for i, j in zip(y_true, y_pred)])))


# ------- BRUTE-FORCE FIND -------#
    
def find(y_true, length=None, rounds=50, no_points=50):
    start_time = time.time()
    results = []    
    for i in range(rounds):
        counter = 0
        found = False
        while not found:
            if found:
                break
            y_pred = [0] * no_points
            found = True
            counter += 1
            builder = Poly_builder(length)
            my_poly = builder.generate()
            for j in range(no_points): # Test for _ points
                y_pred[j] = my_poly.evaluate(j)
                test = y_pred[j] == y_true[j]
                if not test:
                    found = False
        print("Round " + str(i) + ": f(x) = " + str(my_poly.to_string()))
        print("Samples: " + str(counter))
        logging.info("Round " + str(i) + ": f(x) = " + str(my_poly.to_string()))
        logging.info("Samples: " + str(counter))

        end_time = time.time()
        
        logging.info("\nAverage: " + str(np.mean(results)))
        logging.info("Variance: " + str(np.var(results)))
        logging.info("Standard deviation: " + str(np.std(results)))
        logging.info("Elapsed time (s): " + str(end_time - start_time))
        results.append(counter)

    end_time = time.time()
    
    print("\nAverage: " + str(np.mean(results)))
    print("Variance: " + str(np.var(results)))
    print("Standard deviation: " + str(np.std(results)))
    print("Elapsed time (s): " + str(end_time - start_time))
    logging.info("\nAverage: " + str(np.mean(results)))
    logging.info("Variance: " + str(np.var(results)))
    logging.info("Standard deviation: " + str(np.std(results)))
    logging.info("Elapsed time (s): " + str(end_time - start_time))
#------- MAIN -------#

rounds = int(os.getenv('rounds', 10))
no_points = int(os.getenv('points', 50))
expr = os.getenv('expr', "(3 * x + 5) * (2 * x - 6)")

if __name__ == "__main__":
    # log_filename = "log_non-evolutionary" + str(time.time()) + ".log"
    # logging.basicConfig(filename=log_filename, level=logging.INFO)
    y_true = [eval(expr, {"x":x}) for x in range(no_points)]

    print("Polynomial: " + expr)
    logging.info("Polynomial: " + expr)
    print("Rounds: " + str(rounds))
    logging.info("Rounds: " + str(rounds))

    print("N O N - E V O L U T I O N A R Y: \n")
    logging.info("N O N - E V O L U T I O N A R Y: \n")
    find(y_true, length=None, rounds=rounds, no_points=no_points)
    


    
