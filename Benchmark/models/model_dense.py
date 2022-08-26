# -----------------------------------------------------------
# Dense Subclass of Model Class
# -----------------------------------------------------------

from models import Model
import keras
import numpy

class Dense(Model):
    """Keras Dense-Neural-Network Model Wrapper
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
        """Inits Dense Class
        Parameters
        ----------
        none
        """
        self.name = "Dense"
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
        regularizer = keras.regularizers.L1L2(l1=parameters["dense_regularizer_l1"], l2=parameters["dense_regularizer_l2"])
        input_layer = keras.layers.Input(name="input", shape=input_shape)
        hidden_layer = input_layer
        for depth, units in enumerate(parameters["dense_depth_layout"]):
            hidden_layer = keras.layers.Dense(name="hidden_"+str(depth), units=units, activation="relu", kernel_regularizer=regularizer)(hidden_layer)
        output_layer = keras.layers.Dense(name="output", units=parameters["last-layer_units"], activation=parameters["last-layer_activation"])(hidden_layer)
    
        model = keras.models.Model(name="DENSE", inputs=input_layer, outputs=output_layer)

        return model