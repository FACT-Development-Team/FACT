# -----------------------------------------------------------
# Standard Classifiers Subclass of Model Class
# -----------------------------------------------------------

from models import Model
import tensorflow
import keras
import numpy

class KNNC(Model):
    """Sklearn K-Nearest-Neighbors-Classifier Model Wrapper
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
        """Inits KNNC Class
        Parameters
        ----------
        none
        """
        self.name = "KNNC"
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
        from sklearn.neighbors import KNeighborsClassifier
        model = KNeighborsClassifier()
        return model

class GNBC(Model):
    """Sklearn Gaussian-Naive-Bayes-Classifier Model Wrapper
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
        """Inits GNBC Class
        Parameters
        ----------
        none
        """
        self.name = "GNBC"
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
        from sklearn.naive_bayes import GaussianNB
        model = GaussianNB()
        return model

class LSVC(Model):
    """Sklearn Linear-Support-Vector-Machine-Classifier Model Wrapper
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
        """Inits LSVC Class
        Parameters
        ----------
        none
        """
        self.name = "LSVC"
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
        from sklearn.svm import LinearSVC
        model = LinearSVC()
        return model

class DTC(Model):
    """Sklearn Decision-Tree-Classifier Model Wrapper
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
        """Inits DTC Class
        Parameters
        ----------
        none
        """
        self.name = "DTC"
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
        from sklearn.tree import DecisionTreeClassifier
        model = DecisionTreeClassifier()
        return model

class RFC(Model):
    """Sklearn Random-Forest-Classifier Model Wrapper
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
        """Inits RFC Class
        Parameters
        ----------
        none
        """
        self.name = "RFC"
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
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier()
        return model

class GBC(Model):
    """Sklearn Gradient-Boosting-Classifier Model Wrapper
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
        """Inits GBC Class
        Parameters
        ----------
        none
        """
        self.name = "GBC"
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
        from sklearn.ensemble import GradientBoostingClassifier
        model = GradientBoostingClassifier()
        return model

class ABC(Model):
    """Sklearn Ada-Boost-Classifier Model Wrapper
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
        """Inits ABC Class
        Parameters
        ----------
        none
        """
        self.name = "ABC"
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
        from sklearn.ensemble import AdaBoostClassifier
        model = AdaBoostClassifier()
        return model

class XGBC(Model):
    """Sklearn XG-Boost-Classifier Model Wrapper
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
        """Inits XGBC Class
        Parameters
        ----------
        none
        """
        self.name = "XGBC"
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
        from xgboost import XGBClassifier
        model = XGBClassifier()
        return model

class DYC(Model):
    """Sklearn Dummy-Classifier Model Wrapper
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
        """Inits DYC Class
        Parameters
        ----------
        none
        """
        self.name = "DYC"
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
        from sklearn.dummy import DummyClassifier
        model = DummyClassifier()
        return model
