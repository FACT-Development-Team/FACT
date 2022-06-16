from synthetic.generate import Generator
from synthetic.compound import Add, Sub, Mult, Pow
from synthetic.number import Const, NConst, Var
from synthetic.trigonometric import Sin, Cos
from synthetic.prime import Prime
from synthetic.modulo import Modulo
from synthetic.periodic import Periodic
from synthetic.finite import Finite

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

g = Generator(length=4)
poly = g.generate(terminals=terminals, non_terminals=non_terminals)
print('Length: ', poly.get_length())
print(poly.to_string())


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

g = Generator(length=10)
trigo = g.generate(terminals=terminals, non_terminals=non_terminals)
print('Length: ', trigo.get_length())
print(trigo.to_string())

#### Exponential
#------- SET CONTEXT-FREE GRAMMAR -------#
print("EXPONENTIAL")
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
g = Generator(length=10)
exp = g.generate(terminals=terminals, non_terminals=[Pow()])
print('Length: ', exp.get_length())
print(exp.to_string())


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
g = Generator(length=10)
prim = g.generate(terminals=terminals, non_terminals=non_terminals)
print('Length: ', prim.get_length())
print(prim.to_string())


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
print('Length: ', modulo.get_length())
print(modulo.to_string())


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
g = Generator(length=10)
periodic = g.generate(terminals=terminals, non_terminals=[Periodic()])
print('Length: ', periodic.get_length())
print(periodic.to_string())
print([periodic.evaluate(i) for i in range(100)])

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
print('Length: ', finite.get_length())
print(finite.to_string())
print([finite.evaluate(i) for i in range(100)])

#print([eval('exec("import math") or (x + 52 + int(math.cos(math.pi/2 * (689098))))**5', {"x":x}) for x in range(10)])