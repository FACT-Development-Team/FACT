# -----------------------------------------------------------
# RNN Subclass of Model Class
# -----------------------------------------------------------

from models import Model
import keras
import numpy

class RNN(Model):
    """Keras Recurrent-Neural-Network Model Wrapper
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
        """Inits RNN Class
        Parameters
        ----------
        none
        """
        self.name = "RNN"
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
        input_layer = keras.layers.Input(name="input", shape=input_shape)
        lstm_layer = input_layer
        regularizer = keras.regularizers.L1L2(l1=parameters["rnn_regularizer_l1"], l2=parameters["rnn_regularizer_l2"])
        for depth, units in enumerate(parameters["rnn_depth_layout"][:-1]):
            lstm_layer = keras.layers.LSTM(name="lstm_"+str(depth), units=units, return_sequences=True, kernel_regularizer=regularizer, dropout=parameters["rnn_dropout"])(lstm_layer)
        lstm_layer = keras.layers.LSTM(name="lstm_"+str(len(parameters["rnn_depth_layout"])-1), units=parameters["rnn_depth_layout"][-1], return_sequences=False)(lstm_layer)
        output_layer = keras.layers.Dense(name="output", units=parameters["last-layer_units"], activation=parameters["last-layer_activation"])(lstm_layer)
        model = keras.models.Model(name="RNN", inputs=input_layer, outputs=output_layer)
        return model