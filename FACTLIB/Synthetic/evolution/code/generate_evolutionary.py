import sys
import copy
import numpy as np
import time
import os
import logging

from random import randrange, choices, randint
from typing import Union



class Poly_builder():
    def __init__(self, length:int=None, mutation_rate:float=0, crossover_rate:float=0):
        self.options = 1
        self.length = generate_coinflips() if length == None else length
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

    def generate(self, parent=None, current=None):
        mutate = biased_coin(self.mutation_rate)
        if current != None and current.visited:
            return current

        if current == None or mutate:  
            item = self.get_item()
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

    def generate_number(self, parent, current, is_leading:bool):
        mutate = biased_coin(self.mutation_rate)
        if current != None and current.visited:
            return current

        if current == None or mutate:
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
        mutate = biased_coin(self.mutation_rate)
        if current != None and current.visited:
            return current
        if mutate:
            item = Const2() if isinstance(current, Const2) else Const()
            item.set_parent(parent)
            item.visited = True
            item.finish(self)
        else:
            item = current
            item.set_parent(parent)
            item.visited = True
            item.finish(self)
        return item

    def generate_parent(self, child, current):
        mutate = biased_coin(self.mutation_rate)
        if current != None and current.visited:
            return current

        if current == None or mutate:
            item = self.get_item_parent()
            if item == None:
                self.options -= 1
                return item
            item.set_child(child)
            item.visited = True
            self.options += item.get_options() - 1
            self.length -= 1 if item.is_non_terminal() else 0
            item.finish(self)
        else:
            item = current
            item.set_child(child)
            item.visited = True
            self.options += item.get_options() - 1
            self.length -= 1 if item.is_non_terminal() else 0
            item.finish(self)
        return item
            
    def get_item(self):
        coin = biased_coin(1/self.options) and self.length > 0
        crossover = biased_coin(self.crossover_rate)
        if coin:
            library = tournament_non_terminals if crossover and tournament_non_terminals != [] else non_terminals
        else:
            library = tournament_terminals if crossover and tournament_terminals != [] else terminals

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

    def get_item_parent(self):
        coin = biased_coin(1/self.options) and self.length > 0
        valid_parents = [Add(), Sub(), Mult(), Pow()]
        if coin:
            library = valid_parents
            next = randrange(len(library))
            item = copy.deepcopy(library[next])
        else:
            item = None
        return item

    def get_root(self, poly):
        return poly if poly.parent == None else self.get_root(poly.parent)

#------- CLASSES -------#

class Const():
    def __init__(self, arg1=None):
        self.arg1 = arg1
        self.parent = None
        self.visited = False

    def finish(self, poly_builder:Poly_builder):
        if self.arg1 == None:
            self.arg1 = randrange(10)
        self.parent = poly_builder.generate_parent(child=self, current=self.parent)

    def set_parent(self, parent):
        self.parent = parent

    def set_child(self, child):
        coin = biased_coin(0.5)
        if coin or isinstance(self, Pow):
            self.arg1 = child
        else:
            self.arg2 = child

    def get_options(self):
        options = 0
        if self.parent == None or not self.parent.visited:
            options += 1
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
        self.parent = poly_builder.generate_parent(child=self, current=self.parent)

    def set_parent(self, parent):
        self.parent = parent

    def set_child(self, child):
        coin = biased_coin(0.5)
        if coin or isinstance(self, Pow):
            self.arg1 = child
        else:
            self.arg2 = child

    def get_options(self):
        options = 0
        if self.parent == None or not self.parent.visited:
            options += 1
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
        self.visited = False

    def finish(self, poly_builder:Poly_builder):
        self.arg1 = poly_builder.generate_constant(parent=self, current=self.arg1)
        self.arg2 = poly_builder.generate_number(parent=self, current=self.arg2, is_leading=False)
        self.parent = poly_builder.generate_parent(child = self, current=self.parent)
    
    def set_parent(self, parent):
        self.parent = parent

    def set_child(self, child):
        coin = biased_coin(0.5)
        if coin or isinstance(self, Pow):
            self.arg1 = child
        else:
            self.arg2 = child

    def get_options(self):
        options = 0
        if self.arg2 == None or not self.arg2.visited:
            options += 1 
        if self.parent == None or not self.parent.visited:
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
        self.visited = False

    def finish(self, poly_builder:Poly_builder):
        self.parent = poly_builder.generate_parent(child = self, current=self.parent)

    def set_parent(self,parent):
        self.parent = parent

    def set_child(self, child):
        coin = biased_coin(0.5)
        if coin or isinstance(self, Pow):
            self.arg1 = child
        else:
            self.arg2 = child

    def get_options(self):
        options = 0
        if self.parent == None or not self.parent.visited:
            options += 1
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
        self.visited = False

    def finish(self, poly_builder:Poly_builder):
        self.arg1 = poly_builder.generate(parent=self, current=self.arg1)
        self.arg2 = poly_builder.generate(parent=self, current=self.arg2)
        self.parent = poly_builder.generate_parent(child = self, current=self.parent)

    def set_parent(self, parent):
        self.parent = parent

    def set_child(self, child):
        coin = biased_coin(0.5)
        if coin or isinstance(self, Pow):
            self.arg1 = child
        else:
            self.arg2 = child

    def get_options(self):
        options = 0
        if self.arg1 == None or not self.arg1.visited:
            options += 1
        if self.arg2 == None or not self.arg2.visited:
            options += 1
        if self.parent == None or not self.parent.visited:
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
        self.visited = False

    def finish(self, poly_builder:Poly_builder):
        self.arg1 = poly_builder.generate(parent=self, current=self.arg1)
        self.arg2 = poly_builder.generate(parent=self, current=self.arg2)
        self.parent = poly_builder.generate_parent(child = self, current=self.parent)

    def set_parent(self, parent):
        self.parent = parent

    def set_child(self, child):
        coin = biased_coin(0.5)
        if coin or isinstance(self, Pow):
            self.arg1 = child
        else:
            self.arg2 = child

    def get_options(self):
        options = 0
        if self.arg1 == None or not self.arg1.visited:
            options += 1
        if self.arg2 == None or not self.arg2.visited:
            options += 1
        if self.parent == None or not self.parent.visited:
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
        self.visited = False

    def finish(self, poly_builder:Poly_builder):
        self.arg1 = poly_builder.generate(parent=self, current=self.arg1)
        self.arg2 = poly_builder.generate(parent=self, current=self.arg2)
        self.parent = poly_builder.generate_parent(child = self, current=self.parent)

    def set_parent(self, parent):
        self.parent = parent

    def set_child(self, child):
        coin = biased_coin(0.5)
        if coin or isinstance(self, Pow):
            self.arg1 = child
        else:
            self.arg2 = child

    def get_options(self):
        options = 0
        if self.arg1 == None or not self.arg1.visited:
            options += 1
        if self.arg2 == None or not self.arg2.visited:
            options += 1
        if self.parent == None or not self.parent.visited:
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
        self.visited = False

    def finish(self, poly_builder:Poly_builder):
        self.arg1 = poly_builder.generate(parent=self, current=self.arg1)
        self.arg2 = poly_builder.generate_number(parent=self, current=self.arg2, is_leading=True)
        self.parent = poly_builder.generate_parent(child = self, current=self.parent)

    def set_parent(self, parent):
        self.parent = parent

    def set_child(self, child):
        coin = biased_coin(0.5)
        if coin or isinstance(self, Pow):
            self.arg1 = child
        else:
            self.arg2 = child

    def get_options(self):
        options = 0
        if self.arg1 == None or not self.arg1.visited:
            options += 1
        if self.arg2 == None or not self.arg2.visited:
            options += 1
        if self.parent == None or not self.parent.visited:
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

tournament_terminals = []
tournament_non_terminals = []

tournament_set = []

#------- AUXILIARY FUNCTIONS -------#

def biased_coin(p):
    return 0 if p == 0 else choices([0, 1], weights=(1 - p, p), k=1)[0]

def generate_coinflips():
    coin = randint(0, 1)
    return 1 + generate_coinflips() if coin else 0

def mean_squared_error(y_true:list, y_pred:list) -> int:
    return abs((sum([(i - j) * (i - j) for i, j in zip(y_true, y_pred)])))

# ------- EVOLUTIONARY FIND -------#

def update_tournament(population:list, tournament_size):
    tournament_non_terminals.clear()
    tournament_terminals.clear()
    if len(population) >= tournament_size:
        next_gen = sorted(population, key=lambda x: x[1], )[:tournament_size]
    else:
        next_gen = sorted(population, key=lambda x: x[1])

    global tournament_set
    tournament_set = next_gen
    for poly, _ in next_gen:
        split(poly)

def split(poly):
    poly.visited = False
    if poly.is_non_terminal():
        tournament_non_terminals.append(poly)
        split(poly.arg1)
        split(poly.arg2)
    else:
        tournament_terminals.append(poly)

def get_min_mse(population):
    poly, min_mse = min(population, key=lambda x: x[1])
    return poly, min_mse
    
def find(y_true,
        length=None,
        rounds=50,
        no_points=50,
        population_size=100,
        tournament_size=10,
        mutation_rate=0,
        crossover_rate=0):

    start_time = time.time()
    results = []    
    for i in range(rounds):
        min_mse = None
        temp = None
        tournament_non_terminals.clear()
        tournament_terminals.clear()
        tournament_set.clear()

        counter = 0
        found = False
        generations = 0
        while not found:
            population = []
            # print("Generation: " + str(generations))
            generations += 1
            for _ in range(population_size):
                if not found:
                    y_pred = [0] * no_points
                    counter += 1
                    builder = Poly_builder(length, mutation_rate, crossover_rate)
                    my_poly = builder.get_root(builder.generate())
                    y_pred = [my_poly.evaluate(j) for j in range(no_points)]
                    found = True if y_pred == y_true else False
                    MSE = mean_squared_error(y_true, y_pred)
                    population.append((my_poly, MSE))
                else:
                    break

            population += tournament_set
            poly, temp = get_min_mse(population)
            if min_mse == None or temp < min_mse:
                min_mse = temp
                min_poly = poly
            # print(str(generations) + "\t" + str(temp))
            update_tournament(population, tournament_size)
                
        print("Round " + str(i) + ": f(x) = " + str(my_poly.to_string()))
        print("Samples: " + str(counter))
        print("Generations to find solution: " + str(generations))
        logging.info("Round " + str(i) + ": f(x) = " + str(my_poly.to_string()))
        logging.info("Samples: " + str(counter))
        logging.info("Generations to find solution: " + str(generations))

        end_time = time.time()

        results.append(counter)
        logging.info("\nAverage: " + str(np.mean(results)))
        logging.info("Variance: " + str(np.var(results)))
        logging.info("Standard deviation: " + str(np.std(results)))
        logging.info("Elapsed time (s): " + str(end_time - start_time))

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
rounds = int(os.getenv('rounds', 100))
no_points = int(os.getenv('points', 50))
expr = os.getenv('expr', "x**5 - x**2")

population = int(os.getenv('population', 1000))
tournament = int(os.getenv('tournament', 5))
mutation_rate = float(os.getenv('mutation_rate', 0.1))
crossover_rate = float(os.getenv('crossover_rate', 0.3))

if __name__ == "__main__":
    # log_filename = "log_evolutionary" + str(time.time()) + ".log"
    # logging.basicConfig(filename=log_filename, level=logging.INFO)
    y_true = [eval(expr, {"x":x}) for x in range(no_points)]

    print("Polynomial: " + expr)
    print("Population: " + str(population))
    print("Tournament: " + str(tournament))
    print("Mutation rate: " + str(mutation_rate))
    print("Crossover rate: " + str(crossover_rate))
    print("Rounds: " + str(rounds))

    logging.info("Polynomial: " + expr)
    logging.info("Population: " + str(population))
    logging.info("Tournament: " + str(tournament))
    logging.info("Mutation rate: " + str(mutation_rate))
    logging.info("Crossover rate: " + str(crossover_rate))
    logging.info("Rounds: " + str(rounds))

    print("E V O L U T I O N A R Y: \n")
    logging.info("E V O L U T I O N A R Y: \n")
    find(y_true,
        length=None,
        rounds=rounds,
        no_points=no_points,
        population_size=population,
        tournament_size=tournament,
        mutation_rate=mutation_rate,
        crossover_rate=crossover_rate)
