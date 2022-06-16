# -----------------------------------------------------------
# Model Class
#
# Released under GNU Public License (GPL)
# @author Flavio Schenker
# @email flaviosc@student.ethz.ch
# -----------------------------------------------------------

import tensorflow
import keras
import numpy

class Model:
    """This Class ensures the implementation of the build_model() method.
    Attributes
    ----------
    none
    Methods
    -------
    build_model(*parameters):
        ensures the implementation of build_model in the subclasses.
    """
    def __init__(self):
        """Inits Model Class
        Parameters
        ----------
        none
        """
        pass

    def build_model(self, *parameters):
        """Inits Standard_1 Class
        Parameters
        ----------
        *parameters: arbitrary list of arguments.
        """
        raise NotImplementedError("subclass should implement the method build_model()")