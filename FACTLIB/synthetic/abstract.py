from abc import ABC, abstractmethod

class Node(ABC):
    """
    Abstract class that defines the interface how a node should support to be used in conjuction with Generator.
    A node can be a terminal or a non_terminal, which should be specified in is_non_terminal function.
    The node that can be used in Generator to define various grammars, and generator can be used to generate sequences
    at random with Kolmogorov complexity bias.
    """
    terminals = []
    non_terminals = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        for key, value in kwargs.items
            self.key = value

    def finish(self, generator):
        for key in self.kwargs.keys():
            self.key = generator.generate(terminals=Node.terminals, non_terminals=Node.non_terminals, current=self.key)

    def set_terminals(terminals):
        Node.terminals = terminals

    def set_non_terminals(non_terminals):
        Node.non_terminals = non_terminals

    @abc.abstractmethod
    def get_options(self):
        """
        Should return the number of the child nodes (the prudction rule in a grammar) that can be used as non-terminal (and have not been used still).
        """
        raise NotImplementedError("This method must be implemented in the inheriting class")

    @abc.abstractmethod
    def is_non_terminal(self):
        """
        Should specify whether a node is a terminal or non_terminal.
        """
        raise NotImplementedError("This method must be implemented in the inheriting class")

    @abc.abstractmethod
    def evaluate(self, value):
        """
        Should specify how the node can be evaluated. Can use recursively the evaluation function of the subnodes.
        """
        raise NotImplementedError("This method must be implemented in the inheriting class")

    @abc.abstractmethod
    def to_string(self):
        """
        Should specify a string representation for the particular node.
        """
        raise NotImplementedError("This method must be implemented in the inheriting class")

    @abc.abstractmethod
    def get_length(self):
        """
        Defines the length that this node has. Example we have used Sine or Cosine as length 3, whereas a Var() as length 1.
        Should compute recursively by adding the length of the child nodes (and itself).
        """
        raise NotImplementedError("This method must be implemented in the inheriting class")
