# -----------------------------------------------------------
# Standard Regressor Subclass of Model Class
# -----------------------------------------------------------

from models import Model
import tensorflow
import keras
import numpy

class KNNR(Model):
    """Sklearn K-Nearest-Neighbors-Regressor Model Wrapper
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
        """Inits KNNR Class
        Parameters
        ----------
        none
        """
        self.name = "KNNR"
        self.dependency = "Sklearn"

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
        sklearn.Model()
        """
        from sklearn.neighbors import KNeighborsRegressor
        model = KNeighborsRegressor()
        return model

class LIR(Model):
    """Sklearn Linear-Regressor Model Wrapper
    Attributes
    ----------
    name : str
        name of the model
    Methods
    -------
    build_model(parameters, input_shape):
        Implementation of the Model wrapper.
    """
    def __init__(self):
        """Inits LIR Class
        Parameters
        ----------
        none
        """
        self.name = "LIR"
        self.dependency = "Sklearn"

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
        sklearn.Model()
        """
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        return model

class RIR(Model):
    """Sklearn Ridge-Regressor Model Wrapper
    Attributes
    ----------
    name : str
        name of the model
    Methods
    -------
    build_model(parameters, input_shape):
        Implementation of the Model wrapper.
    """
    def __init__(self):
        """Inits RIR Class
        Parameters
        ----------
        none
        """
        self.name = "RIR"
        self.dependency = "Sklearn"

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
        sklearn.Model()
        """
        from sklearn.linear_model import Ridge
        model = Ridge()
        return model

class LAR(Model):
    """Sklearn Lasso-Regressor Model Wrapper
    Attributes
    ----------
    name : str
        name of the model
    Methods
    -------
    build_model(parameters, input_shape):
        Implementation of the Model wrapper.
    """
    def __init__(self):
        """Inits LAR Class
        Parameters
        ----------
        none
        """
        self.name = "LAR"
        self.dependency = "Sklearn"

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
        sklearn.Model()
        """
        from sklearn.linear_model import Lasso
        model = Lasso()
        return model

class ENR(Model):
    """Sklearn Elastic-Net-Regressor Model Wrapper
    Attributes
    ----------
    name : str
        name of the model
    Methods
    -------
    build_model(parameters, input_shape):
        Implementation of the Model wrapper.
    """
    def __init__(self):
        """Inits ENR Class
        Parameters
        ----------
        none
        """
        self.name = "ENR"
        self.dependency = "Sklearn"

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
        sklearn.Model()
        """
        from sklearn.linear_model import ElasticNet
        model = ElasticNet()
        return model

class DTR(Model):
    """Sklearn Decision-Tree-Regressor Model Wrapper
    Attributes
    ----------
    name : str
        name of the model
    Methods
    -------
    build_model(parameters, input_shape):
        Implementation of the Model wrapper.
    """
    def __init__(self):
        """Inits DTR Class
        Parameters
        ----------
        none
        """
        self.name = "DTR"
        self.dependency = "Sklearn"

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
        sklearn.Model()
        """
        from sklearn.tree import DecisionTreeRegressor
        model = DecisionTreeRegressor()
        return model

class RFR(Model):
    """Sklearn Random-Forest-Regressor Model Wrapper
    Attributes
    ----------
    name : str
        name of the model
    Methods
    -------
    build_model(parameters, input_shape):
        Implementation of the Model wrapper.
    """
    def __init__(self):
        """Inits RFR Class
        Parameters
        ----------
        none
        """
        self.name = "RFR"
        self.dependency = "Sklearn"

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
        sklearn.Model()
        """
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor()
        return model

class GBR(Model):
    """Sklearn Gradient-Boosting-Regressor Model Wrapper
    Attributes
    ----------
    name : str
        name of the model
    Methods
    -------
    build_model(parameters, input_shape):
        Implementation of the Model wrapper.
    """
    def __init__(self):
        """Inits GBR Class
        Parameters
        ----------
        none
        """
        self.name = "GBR"
        self.dependency = "Sklearn"

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
        sklearn.Model()
        """
        from sklearn.ensemble import GradientBoostingRegressor
        model = GradientBoostingRegressor()
        return model

class ABR(Model):
    """Sklearn Ada-Boost-Regressor Model Wrapper
    Attributes
    ----------
    name : str
        name of the model
    Methods
    -------
    build_model(parameters, input_shape):
        Implementation of the Model wrapper.
    """
    def __init__(self):
        """Inits ABR Class
        Parameters
        ----------
        none
        """
        self.name = "ABR"
        self.dependency = "Sklearn"

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
        sklearn.Model()
        """
        from sklearn.ensemble import AdaBoostRegressor
        model = AdaBoostRegressor()
        return model

class XGBR(Model):
    """Sklearn XG-Boost-Regressor Model Wrapper
    Attributes
    ----------
    name : str
        name of the model
    Methods
    -------
    build_model(parameters, input_shape):
        Implementation of the Model wrapper.
    """
    def __init__(self):
        """Inits XGBR Class
        Parameters
        ----------
        none
        """
        self.name = "XGBR"
        self.dependency = "Sklearn"

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
        sklearn.Model()
        """
        from xgboost import XGBRegressor
        model = XGBRegressor()
        return model

class DYR(Model):
    """Sklearn Dummy-Regressor Model Wrapper
    Attributes
    ----------
    name : str
        name of the model
    Methods
    -------
    build_model(parameters, input_shape):
        Implementation of the Model wrapper.
    """
    def __init__(self):
        """Inits DYR Class
        Parameters
        ----------
        none
        """
        self.name = "DYR"
        self.dependency = "Sklearn"

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
        sklearn.Model()
        """
        from sklearn.dummy import DummyRegressor
        model = DummyRegressor()
        return model
