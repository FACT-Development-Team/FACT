from abc import ABC, abstractmethod

class Node(ABC):
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
        Bide.non_terminals = non_terminals

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
