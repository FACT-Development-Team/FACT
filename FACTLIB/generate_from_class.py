from synthetic.generate import Generator
from synthetic.compound import Add, Sub, Mult, Pow
from synthetic.number import Const, NConst, Var
from synthetic.trigonometric import Sin, Cos
from synthetic.prime import Prime
from synthetic.modulo import Modulo
from synthetic.periodic import Periodic
from synthetic.finite import Finite
from enum import Enum

ClassType = Enum('ClassType', 'POLYNOMIAL TRIGONOMETRIC EXPONENTIAL PRIME MODULO PERIODIC FINITE')

def generate_polynomial(length):
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

    g = Generator(length=length)
    poly = g.generate(terminals=terminals, non_terminals=non_terminals)
    return poly

def generate_trigonometric(length):
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

    g = Generator(length=length)
    trigo = g.generate(terminals=terminals, non_terminals=non_terminals)
    return trigo

def generate_exponential(length):
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
    g = Generator(length=length)
    exp = g.generate(terminals=terminals, non_terminals=[Pow()])
    return exp

def generate_prime_related(length):
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
    g = Generator(length=length)
    prim = g.generate(terminals=terminals, non_terminals=non_terminals)
    return prim

def generate_modulo(length):
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
    g = Generator(length=10)
    modulo = g.generate(terminals=terminals, non_terminals=non_terminals)
    return modulo

def generate_periodic(length):
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
    g = Generator(length=length)
    periodic = g.generate(terminals=terminals, non_terminals=[Periodic()])
    return periodic

def generate_finite(length):
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
    g = Generator(length=10)
    finite = g.generate(terminals=terminals, non_terminals=[Finite()])
    return finite

#print([eval('exec("import math") or (x + 52 + int(math.cos(math.pi/2 * (689098))))**5', {"x":x}) for x in range(10)])

def generate_from_class(class_type: ClassType, length=None):
    if class_type == ClassType.POLYNOMIAL:
        return generate_polynomial(length)
    elif class_type == ClassType.TRIGONOMETRIC:
        return generate_trigonometric(length)
    elif class_type == ClassType.EXPONENTIAL:
        return generate_exponential(length)
    elif class_type == ClassType.PRIME:
        return generate_prime_related(length)
    elif class_type == ClassType.MODULO:
        return generate_modulo(length)
    elif class_type == ClassType.PERIODIC:
        return generate_periodic(length)
    elif class_type == ClassType.FINITE:
        return generate_finite(length)
    else:
        raise ValueError("Given class cannot be generated from context-free grammar. The framework currently supports only class_types: ClassType.POLYNOMIAL, ClassType.TRIGONOMETRIC, ClassType.EXPONENTIAL, ClassType.PRIME, ClassType.MODULO, ClassType.PERIODIC, ClassType.PERIODIC, ClassType.FINITE. Note that classes like unique, bounded and increasing are not generated with context free grammars, but are meta-categories. ")
