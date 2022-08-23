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
import click

@click.group()
def cli():
    pass

########################################
# Run
@cli.command()
@click.option('-s', '--sequence', type=click.Choice(['polynomial', 'trigonometric', 'exponential', "prime", "modulo", "periodic","finite"]), required=False)
@click.option('-l', '--length', help="Length of the expression that you want to generate.", required=False)
def generate(sequence, length):
    """A simple example how to generate a sequences with FACTLIB. Supported class_type are
    polynomial, trigonometric, exponential, prime, modulo, periodic, finite. Note that classes like unique,
    bounded and increasing are not generated with context free grammars, but are meta-categories.
    """
    if sequence:
        sequence = ClassType[sequence.upper()]
        print(sequence)
        if length:
            expression = generate_from_class(sequence, length=int(length))
        else:
            expression = generate_from_class(sequence)
        print("Expression: ", expression.to_string())
        print("First 10 values: ", [expression.evaluate(i) for i in range(10)])
    else:
        for class_type in ClassType:
            print(class_type)
            expression = generate_from_class(class_type, length=3)
            print(expression.to_string())
            print([expression.evaluate(i) for i in range(10)])


if __name__ == '__main__':
    cli()
