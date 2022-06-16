from tasks import Task
from models import top_k_multiclass, euclidean_distance, contrastive_loss
import tensorflow
import keras
import numpy
import wandb
from wandb.keras import WandbCallback


class Continuation(Task):
    def __init__(self, model, category, category_name, time):
        super().__init__(model, category, category_name, time)
        self.name = "continuation"
        self.test_immediately = True

    def build_model(self, parameters, input_shape):

        input_layer_1 =  keras.layers.Input(name="input_1", shape=input_shape)
        input_layer_2 =  keras.layers.Input(name="input_2", shape=input_shape)

        parameters["last-layer_units"] = parameters["generation_embedding_dim"] # embedding dim
        parameters["last-layer_activation"] = "sigmoid"

        embedding_network = self.model.build_model(parameters, input_shape) # dependent of the model task
        tower_1 = embedding_network(input_layer_1)
        tower_2 = embedding_network(input_layer_2)
        distance_layer = keras.layers.Lambda(name="distance", function=euclidean_distance)([tower_1, tower_2])

        model = keras.models.Model(name="generation_task"+self.model.name, inputs=[input_layer_1, input_layer_2], outputs=distance_layer)

        model.compile(optimizer="adam", loss=contrastive_loss(parameters["margin_distance"]))
        return (model, embedding_network)
        

    def get_train_data(self, dataset, parameters):
        x_train, y_train = dataset.get_train_data(category=self.category, encoding=parameters["encoding"])
        l_train = len(x_train)
        val_fraction = int(l_train*parameters["validation_split"])

        if l_train > 0:
            parameters["batch_size"] = int(max(32, l_train*0.001))
            train_generator = ContDataGenerator(x_train[val_fraction:], y_train[val_fraction:], parameters)
            validation_generator = ContDataGenerator(x_train[:val_fraction], y_train[:val_fraction], parameters)
        else:
            raise ValueError("training set cannot be empty.")

        input_shape = list(x_train.shape)
        input_shape[1] = parameters["generation_seq_len"]
        input_shape = tuple(input_shape)

        return ((train_generator,validation_generator), input_shape)

    def get_test_data(self, test_source, dataset, parameters):
        x_test, y_test = dataset.get_test_data(test_source=test_source, category=self.category, encoding=parameters["encoding"])
        x_train, y_train = dataset.get_train_data(category=self.category, encoding=parameters["encoding"])

        l_test = len(x_test)
        if l_test > 0:
            if parameters["wandb"]:
                wandb.config.update({"batch_size": int(max(32, min(1,l_test*0.01)))}, allow_val_change=True)
            parameters["batch_size"] = int(max(32, min(1,l_test*0.01)))
            test_generator = ContTestGenerator(x_test, x_train, parameters)
        else:
            test_generator = None

        return test_generator

    def train(self, model, train_generator, parameters):
        callback = []
        if parameters["wandb"]:
            callback = [WandbCallback()]
        model.fit(train_generator[0], validation_data=train_generator[1], epochs=parameters["epochs"], callbacks=callback, verbose=1)
        return model

    def test(self, model, optional_model, test_generator, parameters, test_source):

        embedding_network = optional_model
        x_test = test_generator.x_test
        x_train = test_generator.x_train
        print("start embedding test data.")
        embedded_x_test = embedding_network.predict(x_test)
        print("start embedding train data.")
        embedded_x_train = embedding_network.predict(x_train)
        print("done embedding.")

        top_1_rmse_min_average = []
        top_3_rmse_min_average = []
        top_5_rmse_min_average = []

        for i, sequence in enumerate(x_test):
            y_true = sequence[-1]
            test_embedded = embedded_x_test[i]
            distances = numpy.ravel(euclidean_distance([test_embedded, embedded_x_train]).numpy())
            lookup_indices = numpy.argsort(distances)
            top_1_indices = lookup_indices[:1]
            top_3_indices = lookup_indices[:3]
            top_5_indices = lookup_indices[:5]
            predictions_top_1 = x_train[top_1_indices,-1]
            predictions_top_3 = x_train[top_3_indices,-1]
            predictions_top_5 = x_train[top_5_indices,-1]
            top_1_rmse = numpy.sqrt(numpy.square(y_true - predictions_top_1))
            top_1_rmse_min = numpy.min(top_1_rmse)
            top_3_rmse = numpy.sqrt(numpy.square(y_true - predictions_top_3))
            top_3_rmse_min = numpy.min(top_3_rmse)
            top_5_rmse = numpy.sqrt(numpy.square(y_true - predictions_top_5))
            top_5_rmse_min = numpy.min(top_5_rmse)
            top_1_rmse_min_average.append(top_1_rmse_min)
            top_3_rmse_min_average.append(top_3_rmse_min)
            top_5_rmse_min_average.append(top_5_rmse_min)

        top_1_rmse_min_average = numpy.average(numpy.array([top_1_rmse_min_average]))
        top_3_rmse_min_average = numpy.average(numpy.array([top_3_rmse_min_average]))
        top_5_rmse_min_average = numpy.average(numpy.array([top_5_rmse_min_average]))

        print("result top 1", top_1_rmse_min_average)
        print("result top 3", top_3_rmse_min_average)
        print("result top 5", top_5_rmse_min_average)

        if parameters["wandb"]:
            wandb.log({("top 1 rmse "+test_source): top_1_rmse_min_average})
            wandb.log({("top 3 rmse "+test_source): top_3_rmse_min_average})
            wandb.log({("top 5 rmse "+test_source): top_5_rmse_min_average})

        return (top_1_rmse_min_average, top_3_rmse_min_average, top_5_rmse_min_average)

class ContDataGenerator(tensorflow.keras.utils.Sequence):
    def __init__(self, x_all, y_all, parameters):
        self.seq_len = parameters["generation_seq_len"]
        self.batch_size = parameters["batch_size"]
        self.len = int(len(x_all) / 2)
        self.x_left = x_all[:self.len,:self.seq_len]
        self.x_right = x_all[self.len:2*self.len,:self.seq_len]

        self.masking_array = self.x_left == self.x_right
        self.same_or_different = numpy.argmin(self.masking_array, axis=1) / self.seq_len
        self.x_masked = self.x_left * self.masking_array

    def __len__(self):
        return int(self.len / self.batch_size)

    def on_epoch_end(self):
        pass

    def __getitem__(self, index):

        begin = int(index*self.batch_size)
        end = int(begin + self.batch_size)

        # 1) a&b unmasked, 2) a unmasked, a masked 3) b masked, b unmasked
        left_stack = numpy.concatenate((self.x_left[begin:end], self.x_left[begin:end], self.x_masked[begin:end]), axis=0)
        right_stack = numpy.concatenate((self.x_right[begin:end], self.x_masked[begin:end], self.x_right[begin:end]), axis=0)
        same_or_different_stack = numpy.concatenate((self.same_or_different[begin:end], self.same_or_different[begin:end], self.same_or_different[begin:end]), axis=0)

        return ([left_stack, right_stack], same_or_different_stack)

class ContTestGenerator():
    def __init__(self, x_test, x_train, parameters):
        self.seq_len = parameters["generation_seq_len"]
        self.x_test = x_test[:1000,:self.seq_len]
        self.x_train = x_train[:,:self.seq_len]
