# FACTLIB

A library for synthetic generation of integer sequences to the style of OEIS and with the notions of Kolmogorov complexity in mind.

## How to Install
There are no dependencies needed in this repository (other than having Python 3.X). You can directly use this module independently from other parts of the FACT-framework.


## Using FACTLIB

For a quick run, you can simply use the following command:
```python3 main.py
```
The above command should generate an example sequence for each category.

The framework currently supports only class_types: ClassType.POLYNOMIAL, ClassType.TRIGONOMETRIC, ClassType.EXPONENTIAL, ClassType.PRIME, ClassType.MODULO, ClassType.PERIODIC, ClassType.PERIODIC, ClassType.FINITE. Note that classes like unique, bounded and increasing are not generated with context free grammars, but are meta-categories.

An example generating a polynomial of length 3:

```python
from generate_from_class import generate_from_class
from generate_from_class import ClassType

expression = generate_from_class(ClassType.POLYNOMIAL, length=3)
print(expression.to_string())
print([expression.evaluate(i) for i in range(10)])
```

One can also provide as argument `length=None`, in which case FACTLIB generates a polynomial with the length computed based on Universal Prior [1].

## Extending FACTLIB

### Creating a context-free grammar
The backend of FACTLIB has a simple structure where the main object is `Generator` from `synthetic/generate.py`. In simple terms, one defines the context-free grammar by giving the terminal and non-terminal rules.

For example, lets create expressions that contain only one-digit numbers, linear variables and additions. We can use Add(), Var(), and Const().
Add is a non-terminal and we can define its production rule by providing the terminals and non-terminals as here:
```python
terminals = [Var(), Const()]
non_terminals = [Add()]
Add.terminals = terminals
Add.non_terminals = non_terminals
g = Generator(length=length)
add_only_expression = g.generate(terminals=terminals, non_terminals=non_terminals)
```

With the same principle, one can create any context-free grammars. For example, context-free grammar for polynomials looks like:

```python
from synthetic.generate import Generator
from synthetic.compound import Add, Sub, Mult, Pow
from synthetic.number import Const, NConst, Var
from synthetic.trigonometric import Sin, Cos
from synthetic.prime import Prime
from synthetic.modulo import Modulo
from synthetic.periodic import Periodic
from synthetic.finite import Finite

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
```

Note that for constants that have multiple digits we use NConst(). This is desired because we generate expressions with Kolmogorov complexity in mind. The generation and the length of multiple-digit constants can be easily tracked this way.

### Creating new terminals and non-terminals
You can create new terminals and non-terminals by simply following the same structure as any other object. We define the interface to make this easier, one can extend this interface and implement (override) the following functions:
```python
@abc.abstractmethod
def get_options(self):
    raise NotImplementedError("This method must be implemented in the inheriting class")

@abc.abstractmethod
def is_non_terminal(self):
    raise NotImplementedError("This method must be implemented in the inheriting class")

@abc.abstractmethod
def evaluate(self, value):
    raise NotImplementedError("This method must be implemented in the inheriting class")

@abc.abstractmethod
def to_string(self):
    raise NotImplementedError("This method must be implemented in the inheriting class")

@abc.abstractmethod
def get_length(self):
    raise NotImplementedError("This method must be implemented in the inheriting class")
```

## Future steps

FACTLIB has also a `evolution/generate.py`. This is in experimental stages. However it is runnable.
This entry point is a more complex generator, which instead of simply sampling terminals and nonterminals, it also provides evolutionary techniques such as cross-over and mutation.
This is however at this point not part of the main paper.
