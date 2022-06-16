from tasks import Task
import tensorflow
import keras
import numpy
import wandb
from wandb.keras import WandbCallback

class Generation(Task):
    def __init__(self, model, category, category_name, time):
        super().__init__(model, category, category_name, time)
        self.name = "generation"
        self.test_immediately = True

    def build_model(self, parameters, input_shape):

        parameters["last-layer_units"] = 1
        parameters["last-layer_activation"] = "linear"
        #slice input length to 10x5
        input_shape = list(input_shape)
        input_shape[0] = int((input_shape[0] / parameters["continuation_split"]) - 1)
        input_shape = tuple(input_shape)

        model = self.model.build_model(parameters, input_shape)

        if self.model.dependency == "Keras":
            model.compile(optimizer=parameters["optimizer"], loss="mean_squared_logarithmic_error")
        elif self.model.dependency == "Sklearn":
            pass
        else:
            raise ValueError("dependency not supported.")        
        return (model, None)

    def get_train_data(self, dataset, parameters):
        x_train, y_train = dataset.get_train_data(category=self.category, encoding=parameters["encoding"])
        l_train = len(x_train)
        val_fraction = int(l_train*parameters["validation_split"])

        if l_train > 0:
            if self.model.dependency == "Keras":
                parameters["batch_size"] = int(max(32, l_train*0.001))
                train_generator_train = ContinuationDataGenerator(x_train[val_fraction:], y_train[val_fraction:], parameters)
                train_generator_val = ContinuationDataGenerator(x_train[:val_fraction], y_train[:val_fraction], parameters)
                train_generator = (train_generator_train, train_generator_val)
            elif self.model.dependency == "Sklearn":
                train_generator = StandardModelDataGenerator(x_train, parameters["continuation_split"])
            else:
                raise ValueError("dependency not supported.")      
        else:
            raise ValueError("training set cannot be empty.")


        input_shape = x_train.shape
        return (train_generator, input_shape)

    def get_test_data(self, test_source, dataset, parameters):
        x_test, y_test = dataset.get_test_data(test_source=test_source, category=self.category, encoding=parameters["encoding"])
        l_test = len(x_test)
        if l_test > 0:
            if self.model.dependency == "Keras":
                if parameters["wandb"]:
                    wandb.config.update({"batch_size": int(max(1, min(1,l_test*0.01)))}, allow_val_change=True)
                parameters["batch_size"] = int(max(1, min(1,l_test*0.01)))
                test_generator = ContinuationDataGenerator(x_test, y_test, parameters)
            elif self.model.dependency == "Sklearn":
                test_generator = StandardModelDataGenerator(x_test, parameters["continuation_split"])
            else:
                raise ValueError("dependency not supported.")   
        else:
            test_generator = None

        return test_generator

    def train(self, model, train_generator, parameters):

        if self.model.dependency == "Keras":
            callback = []
            if parameters["wandb"]:
                callback = [WandbCallback()]
            model.fit(train_generator[0], validation_data=train_generator[1], epochs=parameters["epochs"], callbacks=callback, verbose=2)
        elif self.model.dependency == "Sklearn":
            x_train, y_train = train_generator
            model.fit(x_train, y_train)
            print("training done.")
        else:
            raise ValueError("dependency not supported.")

        return model

    def test(self, model, optional_model, test_generator, parameters, test_source):

        if self.model.dependency == "Keras":
            test_results = model.evaluate(test_generator, verbose=2)
            if parameters["wandb"]:
                wandb.log({("test msle "+test_source): test_results})
        elif self.model.dependency == "Sklearn":
            print("start evaluation process.")
            x_test, y_test = test_generator
            y_pred = model.predict(x_test)

            test_results = numpy.average(numpy.square((numpy.log(y_pred + 1.0037) - numpy.log(y_test + 1.0037))))
            print("evaluation done.")
            if parameters["wandb"]:
                wandb.log({("test msle "+test_source): test_results.item()})
        else:
            raise ValueError("dependency not supported.")

        return test_results


class ContinuationDataGenerator(tensorflow.keras.utils.Sequence):
    def __init__(self, x_all, y_all, parameters):
        self.x_all = x_all
        self.y_all = y_all
        self.batch_size = parameters["batch_size"]
        self.continuation_split = parameters["continuation_split"]
        self.len = len(x_all)

    def __len__(self):
        return int(self.len / self.batch_size)


    def __getitem__(self, index):

        # only functions for raw input

        batch = self.x_all[index*self.batch_size:(index+1)*self.batch_size]

        # slice each sequence of length 50 into 10 subsequences of 5
        batch = batch.reshape((-1, int(batch.shape[-1]/self.continuation_split)))

        batch_x = batch[:,:-1]
        batch_y = numpy.squeeze(batch[:,-1:])

        return (batch_x, batch_y)

def StandardModelDataGenerator(x_all, continuation_split):
    batch = x_all.reshape((-1, int(x_all.shape[-1]/continuation_split)))

    batch_x = batch[:,:-1]
    batch_y = numpy.squeeze(batch[:,-1:])

    return (batch_x, batch_y)