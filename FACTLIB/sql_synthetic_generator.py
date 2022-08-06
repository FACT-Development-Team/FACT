from re import S
from synthetic.generate import Generator
from synthetic.compound import Add, Sub, Mult, Pow
from synthetic.number import Const, NConst, Var
from synthetic.trigonometric import Sin, Cos
from synthetic.prime import Prime
from synthetic.modulo import Modulo
from synthetic.periodic import Periodic
from synthetic.finite import Finite


polynomial_group = 0
trigonometric_group = 10000000
exponential_group = 20000000
modulo_group = 30000000
prime_group = 40000000
periodic_group = 50000000
finite_group = 60000000
math_group = 70000000

def generate_synthetic_polynomial(counter, length):
    ### POLYNOMIALS
    terminals = [Var(), Const()]
    non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow()]
    Add.terminals = terminals
    Add.non_terminals = non_terminals
    Sub.terminals = terminals
    Sub.non_terminals = non_terminals
    Mult.terminals = terminals
    Mult.non_terminals = non_terminals
    Pow.terminals_base = terminals
    Pow.non_terminals_base = non_terminals
    Pow.terminals_exponent = [Const()]
    Pow.non_terminals_exponent = [NConst(positive=True)]
    group = polynomial_group
    invalid = True
    poly = None
    values = None

    while invalid:
        g = Generator(length=length)
        poly = g.generate(terminals=terminals, non_terminals=non_terminals)
        values = []
        for j in range(500):
            next = poly.evaluate(j)
            if abs(next) > 999999999999999:
                break
            values.append(next)
        if len(values) == 500:
            invalid = False
        
    entry = (
    -counter, 
    "S PO G " + str(counter), 
    str(values)[1:-1], 
    "Polynomial of length " + str(poly.get_length()) + " and node length " + str(length + 1), 
    """ terminals = [Var(), Const()]
        non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow()]
        Add.terminals = terminals
        Add.non_terminals = non_terminals
        Sub.terminals = terminals
        Sub.non_terminals = non_terminals
        Mult.terminals = terminals
        Mult.non_terminals = non_terminals
        Pow.terminals_base = terminals
        Pow.non_terminals_base = non_terminals
        Pow.terminals_exponent = [Const()]
        Pow.non_terminals_exponent = [NConst(positive=True)]""",
    "",
    "",
    poly.to_string(),
    "",
    "",
    "",
    poly.to_string(),
    "",
    "synthetic,polynomial",
    0,
    0,
    "Ard Kastrati",
    "")

    return entry

def generate_synthetic_trigonometric(counter, length):
    #### TRIGONOMETRIC
    #------- SET CONTEXT-FREE GRAMMAR -------#
    terminals = [Var(), Const()]
    non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow(), Sin(), Cos()]
    Add.terminals = terminals
    Add.non_terminals = non_terminals
    Sub.terminals = terminals
    Sub.non_terminals = non_terminals
    Mult.terminals = terminals
    Mult.non_terminals = non_terminals
    Pow.terminals_base = terminals
    Pow.non_terminals_base = non_terminals
    Pow.terminals_exponent = [Const()]
    Pow.non_terminals_exponent = [NConst(positive=True)]
    Sin.terminals = terminals
    Sin.non_terminals = non_terminals
    Cos.terminals = terminals
    Cos.non_terminals = non_terminals


    group = trigonometric_group

    invalid = True
    trigo = None
    values = None

    while invalid:
        g = Generator(length=length)
        trigo = g.generate(terminals=terminals, non_terminals=non_terminals)
        values = []
        if trigo.to_string().find("math") != -1:
            for j in range(500):
                next = trigo.evaluate(j)
                if abs(next) > 999999999999999:
                    break
                values.append(next)
        if len(values) == 500:
            invalid = False
        
    entry = (
    - group - counter, 
    "S TR B " + str(i), 
    str(values)[1:-1], 
    "Trigonometric of length " + str(trigo.get_length()) + " and node length " + str(length + 1), 
    """ terminals = [Var(), Const()]
        non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow(), Sin(), Cos()]
        Add.terminals = terminals
        Add.non_terminals = non_terminals
        Sub.terminals = terminals
        Sub.non_terminals = non_terminals
        Mult.terminals = terminals
        Mult.non_terminals = non_terminals
        Pow.terminals_base = terminals
        Pow.non_terminals_base = non_terminals
        Pow.terminals_exponent = [Const()]
        Pow.non_terminals_exponent = [NConst(positive=True)]
        Sin.terminals = terminals
        Sin.non_terminals = non_terminals
        Cos.terminals = terminals
        Cos.non_terminals = non_terminals""",
    "",
    "",
    trigo.to_string(),
    "",
    "",
    "",
    trigo.to_string(),
    "",
    "synthetic,trigonometric",
    0,
    0,
    "Ard Kastrati",
    "")

    return entry

def thread_evaluate(exp, j, answer):
    s = exp.evaluate(j)
    answer[0] = s

def generate_synthetic_exponential(counter, length):
    #### Exponential
    #------- SET CONTEXT-FREE GRAMMAR -------#
    terminals = [Var(), Const()]
    non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow()]
    Add.terminals = terminals
    Add.non_terminals = non_terminals
    Sub.terminals = terminals
    Sub.non_terminals = non_terminals
    Mult.terminals = terminals
    Mult.non_terminals = non_terminals
    Pow.terminals_base = terminals
    Pow.non_terminals_base = non_terminals
    Pow.terminals_exponent = terminals
    Pow.non_terminals_exponent = non_terminals

    group = exponential_group
        
    invalid = True
    exp = None
    values = None

    while invalid:
        g = Generator(length=length)
        exp = g.generate(terminals=terminals, non_terminals=non_terminals)
        values = []
        if exp.to_string().find("**(") != -1:
            for j in range(50):
                import multiprocessing
                import time
                manager = multiprocessing.Manager()
                answer = manager.dict()
                p = multiprocessing.Process(target=thread_evaluate, args=(exp, j, answer))
                p.start()
                p.join(1)
                if p.is_alive():
                    #print("running... let's kill it...")
                    #print(exp.to_string())
                    #print(len(values))
                    p.kill()
                    break
                else:
                    next = answer[0]
                    if not isinstance(next, int) or abs(next) > 999999999999999:
                        break
                    values.append(next)
        if len(values) > 10:
            invalid = False
        
    entry = (
    - group - counter, 
    "S EX G " + str(counter), 
    str(values)[1:-1], 
    "Exponential of length " + str(exp.get_length()) + " and node length " + str(length + 1), 
    """ terminals = [Var(), Const()]
        non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow()]
        Add.terminals = terminals
        Add.non_terminals = non_terminals
        Sub.terminals = terminals
        Sub.non_terminals = non_terminals
        Mult.terminals = terminals
        Mult.non_terminals = non_terminals
        Pow.terminals_base = terminals
        Pow.non_terminals_base = non_terminals
        Pow.terminals_exponent = terminals
        Pow.non_terminals_exponent = non_terminals""",
    "",
    "",
    exp.to_string(),
    "",
    "",
    "",
    exp.to_string(),
    "",
    "synthetic,exponential",
    0,
    0,
    "Ard Kastrati",
    "")
    return entry


def generate_synthetic_modulo(counter, length):
    #### Modulo
    #------- SET CONTEXT-FREE GRAMMAR -------#
    terminals = [Var(), Const()]
    non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow(), Modulo()]
    Add.terminals = terminals
    Add.non_terminals = non_terminals
    Sub.terminals = terminals
    Sub.non_terminals = non_terminals
    Mult.terminals = terminals
    Mult.non_terminals = non_terminals
    Pow.terminals_base = terminals
    Pow.non_terminals_base = non_terminals
    Pow.terminals_exponent = terminals
    Pow.non_terminals_exponent = non_terminals
    Modulo.terminals = terminals
    Modulo.non_terminals = non_terminals

    group = modulo_group
        
    invalid = True
    modulo = None
    values = None

    while invalid:
        g = Generator(length=length)
        modulo = g.generate(terminals=terminals, non_terminals=non_terminals)
        values = []
        if modulo.to_string().find("mod") != -1:
            for j in range(500):
                import multiprocessing
                import time
                manager = multiprocessing.Manager()
                answer = manager.dict()
                p = multiprocessing.Process(target=thread_evaluate, args=(modulo, j, answer))
                p.start()
                p.join(1)
                if p.is_alive():
                    print("running... let's kill it...")
                    #print(exp.to_string())
                    #print(len(values))
                    p.kill()
                    break
                else:
                    next = answer[0]
                    if not isinstance(next, int) or abs(next) > 999999999999999:
                        break
                    values.append(next)
        if len(values) == 500:
            invalid = False
        
    entry = (
    - group - counter, 
    "S MO G " + str(counter), 
    str(values)[1:-1], 
    "Modulo of length " + str(modulo.get_length()) + " and node length " + str(length + 1), 
    """ terminals = [Var(), Const()]
        non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow(), Modulo()]
        Add.terminals = terminals
        Add.non_terminals = non_terminals
        Sub.terminals = terminals
        Sub.non_terminals = non_terminals
        Mult.terminals = terminals
        Mult.non_terminals = non_terminals
        Pow.terminals_base = terminals
        Pow.non_terminals_base = non_terminals
        Pow.terminals_exponent = terminals
        Pow.non_terminals_exponent = non_terminals
        Modulo.terminals = terminals
        Modulo.non_terminals = non_terminals""",
    "",
    "",
    modulo.to_string(),
    "",
    "",
    "",
    modulo.to_string(),
    "",
    "synthetic,modulo",
    0,
    0,
    "Ard Kastrati",
    "")
    return entry


def generate_synthetic_prime(counter, length):
    #### Prime Related
    #------- SET CONTEXT-FREE GRAMMAR -------#
    terminals = [Var(), Const()]
    non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow(), Prime()]
    Add.terminals = terminals
    Add.non_terminals = non_terminals
    Sub.terminals = terminals
    Sub.non_terminals = non_terminals
    Mult.terminals = terminals
    Mult.non_terminals = non_terminals
    Pow.terminals_base = terminals
    Pow.non_terminals_base = non_terminals
    Pow.terminals_exponent = terminals
    Pow.non_terminals_exponent = non_terminals
    Prime.terminals = [Var()]
    Prime.non_terminals = None

    group = prime_group
        
    invalid = True
    prime = None
    values = None

    while invalid:
        g = Generator(length=length)
        prime = g.generate(terminals=terminals, non_terminals=non_terminals)
        values = []
        if prime.to_string().find("prime") != -1:
            for j in range(500):
                import multiprocessing
                import time
                manager = multiprocessing.Manager()
                answer = manager.dict()
                p = multiprocessing.Process(target=thread_evaluate, args=(prime, j, answer))
                p.start()
                p.join(1)
                if p.is_alive():
                    print("running... let's kill it...")
                    #print(exp.to_string())
                    #print(len(values))
                    p.kill()
                    break
                else:
                    next = answer[0]
                    if not isinstance(next, int) or abs(next) > 999999999999999:
                        break
                    values.append(next)
        if len(values) == 500:
            invalid = False
        
    entry = (
    - group - counter, 
    "S PR G " + str(counter), 
    str(values)[1:-1], 
    "Prime related of length " + str(prime.get_length()) + " and node length " + str(length + 1), 
    """ terminals = [Var(), Const()]
        non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow(), Prime()]
        Add.terminals = terminals
        Add.non_terminals = non_terminals
        Sub.terminals = terminals
        Sub.non_terminals = non_terminals
        Mult.terminals = terminals
        Mult.non_terminals = non_terminals
        Pow.terminals_base = terminals
        Pow.non_terminals_base = non_terminals
        Pow.terminals_exponent = terminals
        Pow.non_terminals_exponent = non_terminals
        Prime.terminals = [Var()]
        Prime.non_terminals = None""",
    "",
    "",
    prime.to_string(),
    "",
    "",
    "",
    prime.to_string(),
    "",
    "synthetic,prime",
    0,
    0,
    "Ard Kastrati",
    "")
    return entry



def generate_synthetic_periodic(counter, length):
    #### Periodic
    #------- SET CONTEXT-FREE GRAMMAR -------#
    terminals = [Var(), Const()]
    non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow()]
    Add.terminals = terminals
    Add.non_terminals = non_terminals
    Sub.terminals = terminals
    Sub.non_terminals = non_terminals
    Mult.terminals = terminals
    Mult.non_terminals = non_terminals
    Pow.terminals_base = terminals
    Pow.non_terminals_base = non_terminals
    Pow.terminals_exponent = terminals
    Pow.non_terminals_exponent = non_terminals
    Periodic.terminals = terminals
    Periodic.non_terminals = non_terminals

    group = periodic_group
        
    invalid = True
    periodic = None
    values = None

    while invalid:
        g = Generator(length=length)
        periodic = g.generate(terminals=terminals, non_terminals=[Periodic()])
        values = []
        if periodic.to_string().find("periodic") != -1:
            for j in range(500):
                import multiprocessing
                import time
                manager = multiprocessing.Manager()
                answer = manager.dict()
                p = multiprocessing.Process(target=thread_evaluate, args=(periodic, j, answer))
                p.start()
                p.join(1)
                if p.is_alive():
                    print("running... let's kill it...")
                    #print(exp.to_string())
                    #print(len(values))
                    p.kill()
                    break
                else:
                    next = answer[0]
                    if not isinstance(next, int) or abs(next) > 999999999999999:
                        break
                    values.append(next)
        if len(values) == 500:
            invalid = False
        
    entry = (
    - group - counter, 
    "S PE G " + str(counter), 
    str(values)[1:-1], 
    "Periodic of length " + str(periodic.get_length()) + " and node length " + str(length + 1), 
    """ terminals = [Var(), Const()]
        non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow()]
        Add.terminals = terminals
        Add.non_terminals = non_terminals
        Sub.terminals = terminals
        Sub.non_terminals = non_terminals
        Mult.terminals = terminals
        Mult.non_terminals = non_terminals
        Pow.terminals_base = terminals
        Pow.non_terminals_base = non_terminals
        Pow.terminals_exponent = terminals
        Pow.non_terminals_exponent = non_terminals
        Periodic.terminals = terminals
        Periodic.non_terminals = non_terminals""",
    "",
    "",
    periodic.to_string(),
    "",
    "",
    "",
    periodic.to_string(),
    "",
    "synthetic,periodic",
    0,
    0,
    "Ard Kastrati",
    "")
    return entry

def generate_synthetic_finite(counter, length):
    #### Finite
    #------- SET CONTEXT-FREE GRAMMAR -------#
    terminals = [Var(), Const()]
    non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow()]
    Add.terminals = terminals
    Add.non_terminals = non_terminals
    Sub.terminals = terminals
    Sub.non_terminals = non_terminals
    Mult.terminals = terminals
    Mult.non_terminals = non_terminals
    Pow.terminals_base = terminals
    Pow.non_terminals_base = non_terminals
    Pow.terminals_exponent = terminals
    Pow.non_terminals_exponent = non_terminals
    Finite.terminals = terminals
    Finite.non_terminals = non_terminals

    group = finite_group
        
    invalid = True
    finite = None
    values = None

    while invalid:
        g = Generator(length=length)
        finite = g.generate(terminals=terminals, non_terminals=[Finite()])
        values = []
        if finite.to_string().find("finite") != -1:
            for j in range(500):
                import multiprocessing
                import time
                manager = multiprocessing.Manager()
                answer = manager.dict()
                p = multiprocessing.Process(target=thread_evaluate, args=(finite, j, answer))
                p.start()
                p.join(1)
                if p.is_alive():
                    print("running... let's kill it...")
                    #print(exp.to_string())
                    #print(len(values))
                    p.kill()
                    break
                else:
                    next = answer[0]
                    if not isinstance(next, int) or abs(next) > 999999999999999:
                        break
                    values.append(next)
        if len(values) > 5:
            invalid = False
        
    entry = (
    - group - counter, 
    "S FI G " + str(counter), 
    str(values)[1:-1], 
    "Finite of length " + str(finite.get_length()) + " and node length " + str(length + 1), 
    """ terminals = [Var(), Const()]
        non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow()]
        Add.terminals = terminals
        Add.non_terminals = non_terminals
        Sub.terminals = terminals
        Sub.non_terminals = non_terminals
        Mult.terminals = terminals
        Mult.non_terminals = non_terminals
        Pow.terminals_base = terminals
        Pow.non_terminals_base = non_terminals
        Pow.terminals_exponent = terminals
        Pow.non_terminals_exponent = non_terminals
        Finite.terminals = terminals
        Finite.non_terminals = non_terminals""",
    "",
    "",
    finite.to_string(),
    "",
    "",
    "",
    finite.to_string(),
    "",
    "synthetic,finite",
    0,
    0,
    "Ard Kastrati",
    "")
    return entry


# For Peter!
def generate_synthetic_group(counter, length):

    # Generate a sequence of integers from math groups with some "symbol length"
    # values = [the values of the sequence]
    values = [0, 1, 2, 3]
    entry = (
    - math_group - counter, 
    "S GR G " + str(counter), 
    str(values)[1:-1], 
    "Math group of length " + str(length), 
    """ INFORMATION ABOUT GENERATION SHOULD BE HERE""",
    "",
    "",
    "FORMULA OF THE GROUP SHOULD BE HERE",
    "",
    "",
    "",
    "THE PROGRAM THAT GENERATES THE GROUP SEQUENCE SHOULD BE HERE",
    "",
    "synthetic,group",
    0,
    0,
    "Peter Belcak",
    "")
    return entry

print(generate_synthetic_group(20, 20))
#print(generate_synthetic_modulo(100, 5))
#print(generate_synthetic_prime(100, 5))
#print(generate_synthetic_periodic(100, 5))
#print(generate_synthetic_finite(100, 5))