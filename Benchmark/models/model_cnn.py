# -----------------------------------------------------------
# CNN Subclass of Model Class
#
# Released under GNU Public License (GPL)
# @author Flavio Schenker
# @email flaviosc@student.ethz.ch
# -----------------------------------------------------------

from models import Model
import keras
import numpy

class CNN(Model):
    """Keras Convolutional-Neural-Network Model Wrapper
    Attributes
    ----------
    name : str
        Name of the model.
    dependency: str
        Keras or Sklearn, source of the Model wrapper.
    Methods
    -------
    build_model(parameters, input_shape):
        Implementation of the Model wrapper.
    """
    def __init__(self):
        """Inits CNN Class
        Parameters
        ----------
        none
        """
        self.name = "CNN"
        self.dependency = "Keras"

    def build_model(self, parameters, input_shape):
        """Implementation of the Model wrapper.
        Parameters
        ----------
        parameters : dict
            Layout blueprint for the models like 'layer_depth', 'units', etc.
        input_shape: tuple
            Shape of the input training data.
        Returns
        -------
        keras.Model()
        """
        if len(input_shape) < 2:
            input_shape += (1,)
        regularizer = keras.regularizers.L1L2(l1=parameters["cnn_regularizer_l1"], l2=parameters["cnn_regularizer_l2"])
        input_layer = keras.layers.Input(name="input", shape=input_shape)
        pooling_layer = input_layer
        for depth, units in enumerate(parameters["cnn_depth_layout"]):
            conv_layer = keras.layers.Conv1D(name="conv_"+str(depth), filters=parameters["cnn_filters"], kernel_size=parameters["cnn_kernel_size"], kernel_regularizer=regularizer, padding="valid")(pooling_layer)
            pooling_layer = keras.layers.MaxPooling1D(name="pooling_"+str(depth), pool_size=units[0], strides=units[1], padding="valid")(conv_layer)
        flatten_layer = keras.layers.Flatten(name="flatten")(pooling_layer)
        output_layer = keras.layers.Dense(name="output", units=parameters["last-layer_units"], activation=parameters["last-layer_activation"])(flatten_layer)
        model = keras.models.Model(name="CNN", inputs=input_layer, outputs=output_layer)
        return model
