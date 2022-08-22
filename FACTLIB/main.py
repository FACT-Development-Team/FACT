from synthetic.generate import Generator
from synthetic.compound import Add, Sub, Mult, Pow
from synthetic.number import Const, NConst, Var
from synthetic.trigonometric import Sin, Cos
from synthetic.prime import Prime
from synthetic.modulo import Modulo
from synthetic.periodic import Periodic
from synthetic.finite import Finite

from generate_from_class import generate_from_class
from generate_from_class import ClassType

"""
A simple example how to generate a sequence with length 3 from every class type.
"""
for class_type in ClassType:
    expression = generate_from_class(class_type, length=3)
    print(class_type)
    print(expression.to_string())
    print([expression.evaluate(i) for i in range(10)])
