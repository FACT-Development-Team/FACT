from tasks import Task
from models import f1_multiclass_metric
import tensorflow
import keras
import numpy
import wandb
from sklearn.metrics import classification_report, f1_score, confusion_matrix
from wandb.keras import WandbCallback

class Classification(Task):
    def __init__(self, model, category, category_name, time):
        super().__init__(model, category, category_name, time)
        self.name = "classification"
        self.test_immediately = True
        if isinstance(self.category, list):
            self.multi = True
        else:
            self.multi = False

    def build_model(self, parameters, input_shape):

        if self.multi:
            parameters["last-layer_units"] = len(self.category)
        else:
            parameters["last-layer_units"] = 1
        parameters["last-layer_activation"] = "sigmoid"

        model = self.model.build_model(parameters, input_shape)
        if self.model.dependency == "Keras":
            if self.multi:
                model.compile(optimizer="adam", loss="binary_crossentropy", metrics=[f1_multiclass_metric])
            else:
                model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["binary_accuracy"])
        elif self.model.dependency == "Sklearn":
            pass
        else:
            raise ValueError("dependency not supported.")
        return (model, None)

    def get_train_data(self, dataset, parameters):
        x_train, y_train = dataset.get_train_data(category=self.category , encoding=parameters["encoding"])
        return ((x_train, y_train), x_train.shape)

    def get_test_data(self, test_source, dataset, parameters):
        x_test, y_test = dataset.get_test_data(test_source=test_source, category=self.category, encoding=parameters["encoding"])

        l_test = len(x_test)
        if l_test > 0:
            if parameters["wandb"]:
                wandb.config.update({"batch_size": int(max(32, min(1,l_test*0.01)))}, allow_val_change=True)
            parameters["batch_size"] = int(max(32, min(1,l_test*0.01)))
            test_generator = (x_test, y_test)
        else:
            test_generator = None

        return test_generator

    def train(self, model, train_generator, parameters):
        x_train, y_train = train_generator

        if self.model.dependency == "Keras":
            l_train = len(x_train)
            parameters["batch_size"] = int(max(32, l_train*0.0001))
            callback = []
            if parameters["wandb"]:
                callback = [WandbCallback()]
            model.fit(x=x_train, y=y_train, epochs=parameters["epochs"], batch_size=parameters["batch_size"], validation_split=parameters["validation_split"], callbacks=callback, verbose=2)
        elif self.model.dependency == "Sklearn":
            model.fit(x_train, y_train)
        else:
            raise ValueError("dependency not supported.")

        return model

    def test(self, model, optional_model, test_generator, parameters, test_source):
        x_test, y_test = test_generator

        if self.model.dependency == "Keras":
            l_test = len(x_test)
            if parameters["wandb"]:
                wandb.config.update({"batch_size": int(max(32, min(1,l_test*0.01)))}, allow_val_change=True)
            parameters["batch_size"] = int(max(32, min(1,l_test*0.01)))
            if self.multi:
                model.compile(optimizer="adam", loss="binary_crossentropy", metrics=[f1_multiclass_metric])
                y_pred = numpy.where(model.predict(x_test) > 0.5, 1, 0)
                test_results = classification_report(y_test, y_pred, target_names=["polynomial", "exponential", "trigonometric", "periodic", "finite", "modulo", "prime", "bounded", "increasing", "unique"], zero_division=1)
                if parameters["wandb"]:
                    wandb.log({"report": test_results})
            else:
                model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["binary_accuracy"])
                test_results = model.evaluate(x=x_test, y=y_test, batch_size=parameters["batch_size"], verbose=2)
                if parameters["wandb"]:
                    wandb.log({("test acc. "+test_source): test_results[1]})
        elif self.model.dependency == "Sklearn":
            if self.multi:
                test_results = None
            else:
                test_results = model.score(x_test, y_test)
                if parameters["wandb"]:
                    wandb.log({("test acc. "+test_source): test_results.item()})
        else:
            raise ValueError("dependency not supported.")
      
        return test_results