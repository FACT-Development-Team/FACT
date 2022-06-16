from tasks import Task
from models import f1_multiclass_metric
import tensorflow
import keras
import numpy
import wandb
from wandb.keras import WandbCallback

class Next(Task):
    def __init__(self, model, category, category_name, time):
        super().__init__(model, category, category_name, time)
        self.name = "next"
        self.test_immediately = True
        if isinstance(self.category, list):
            self.multi = True
        else:
            self.multi = False

    def build_model(self, parameters, input_shape):

        parameters["last-layer_units"] = 1
        parameters["last-layer_activation"] = "sigmoid"

        half_input_shape = list(input_shape)
        half_input_shape[0] = int(half_input_shape[0]/2)
        half_input_shape = tuple(half_input_shape)

        input_layer_1 =  keras.layers.Input(name="first_sequence", shape=half_input_shape)
        input_layer_2 =  keras.layers.Input(name="second_sequence", shape=half_input_shape)
        concatenate = keras.layers.Concatenate(name="merge")([input_layer_1, input_layer_2])
        network = self.model.build_model(parameters, input_shape)
        output_layer = network(concatenate)
        model = keras.models.Model(name="next_task_"+self.model.name, inputs=[input_layer_1, input_layer_2], outputs=output_layer)

        if self.multi:
            model.compile(optimizer="adam", loss="binary_crossentropy", metrics=[f1_multiclass_metric])
        else:
            model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["binary_accuracy"])
        return (model, network)

    def get_train_data(self, dataset, parameters):
        x_train, y_train = dataset.get_train_data(category=self.category, encoding=parameters["encoding"])
        l_train = len(x_train)
        val_fraction = int(l_train*parameters["validation_split"])

        if l_train > 0:
            parameters["batch_size"] = int(max(32, l_train*0.001))
            train_generator = NextDataGenerator(x_train[val_fraction:], y_train[val_fraction:], parameters)
            validation_generator = NextDataGenerator(x_train[:val_fraction], y_train[:val_fraction], parameters)
        else:
            raise ValueError("training set cannot be empty.")

        input_shape = x_train.shape
        return ((train_generator,validation_generator), input_shape)

    def get_test_data(self, test_source, dataset, parameters):
        x_test, y_test = dataset.get_test_data(test_source=test_source, category=self.category, encoding=parameters["encoding"])
        l_test = len(x_test)
        if l_test > 0:
            if parameters["wandb"]:
                wandb.config.update({"batch_size": int(max(32, min(1,l_test*0.01)))}, allow_val_change=True)
            parameters["batch_size"] = int(max(32, min(1,l_test*0.01)))
            test_generator = NextDataGenerator(x_test, y_test, parameters)
        else:
            test_generator = None

        return test_generator


    def train(self, model, train_generator, parameters):
        callback = []
        if parameters["wandb"]:
            callback = [WandbCallback()]
        model.fit(train_generator[0], validation_data=train_generator[1], epochs=parameters["epochs"], callbacks=callback, verbose=2)
        return model

    def test(self, model, optional_model, test_generator, parameters, test_source):
        if self.multi:
            model.compile(optimizer="adam", loss="binary_crossentropy", metrics=[f1_multiclass_metric])
        else:
            model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["binary_accuracy"])
        test_results = model.evaluate(test_generator, verbose=2)
        if parameters["wandb"]:
            wandb.log({"test accuracy": test_results[1]})
        return test_results


class NextDataGenerator(tensorflow.keras.utils.Sequence):
    def __init__(self, x_all, y_all, parameters):
        self.x_all = x_all
        self.y_all = y_all
        if parameters["batch_size"] < 4:
            raise ValueError("batch size must be at least 4.")
        else:
            self.batch_size = parameters["batch_size"]
        self.parameters = parameters
        self.len = len(x_all)
        self.seq_len = len(x_all[0])
        self.split = int(self.seq_len/2)


        self.left = numpy.stack(numpy.split(x_all, 2, axis=-1))
        self.right = numpy.copy(x_all)
        numpy.random.shuffle(self.right)
        self.right = numpy.stack(numpy.split(self.right, 2, axis=-1))

    def __len__(self):
        return int(len(self.x_all) / (self.batch_size / 4))

    def __getitem__(self, index):

        # take batchsize / 4 samples
        begin = int(index*self.batch_size/4)
        end = int(begin + self.batch_size/4)
        if end > self.len:
            end = self.len

        batch_left_1 = self.left[0, begin:end]
        batch_left_2 = self.left[1, begin:end]
        batch_right_1 = self.right[0, begin:end]
        batch_right_2 = self.right[1, begin:end]

        batch_left = numpy.concatenate((batch_left_1, batch_right_1, batch_left_1, batch_right_1), axis=0)
        batch_right = numpy.concatenate((batch_left_2, batch_right_2, batch_right_2, batch_left_2), axis=0)
        batch_y = numpy.concatenate((numpy.ones(len(batch_left_1)), numpy.ones(len(batch_right_1)), numpy.zeros(len(batch_left_1)), numpy.zeros(len(batch_right_1))))

        return ([batch_left, batch_right], batch_y)