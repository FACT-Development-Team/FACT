from tasks import Task
from models import top_k_multiclass, euclidean_distance, contrastive_loss
import tensorflow
import keras
import numpy
import wandb
from wandb.keras import WandbCallback


class Unmasking(Task):
    def __init__(self, model, category, category_name, time):
        super().__init__(model, category, category_name, time)
        self.name = "unmasking"
        self.test_immediately = True

    def build_model(self, parameters, input_shape):

        input_layer_unmasked =  keras.layers.Input(name="input_unmasked", shape=input_shape)
        input_layer_masked =  keras.layers.Input(name="input_masked", shape=input_shape)

        parameters["last-layer_units"] = parameters["unmasking_embedding_dim"] # embedding dim
        parameters["last-layer_activation"] = "sigmoid"

        embedding_network = self.model.build_model(parameters, input_shape) # dependent of the model task
        tower_1 = embedding_network(input_layer_unmasked)
        tower_2 = embedding_network(input_layer_masked)
        distance_layer = keras.layers.Lambda(name="distance", function=euclidean_distance)([tower_1, tower_2])

        model = keras.models.Model(name="unmasking_task_"+self.model.name, inputs=[input_layer_unmasked, input_layer_masked], outputs=distance_layer)

        model.compile(optimizer="adam", loss=contrastive_loss(parameters["margin_distance"]))
        return (model, embedding_network)
        

    def get_train_data(self, dataset, parameters):
        x_train, y_train = dataset.get_train_data(category=self.category, encoding=parameters["encoding"])
        l_train = len(x_train)
        val_fraction = int(l_train*parameters["validation_split"])

        if l_train > 0:
            parameters["batch_size"] = int(max(32, l_train*0.001))
            train_generator = UnmaskingDataGenerator(x_train[val_fraction:], y_train[val_fraction:], parameters)
            validation_generator = UnmaskingDataGenerator(x_train[:val_fraction], y_train[:val_fraction], parameters)
        else:
            raise ValueError("training set cannot be empty.")

        input_shape = list(x_train.shape)
        input_shape[1] = parameters["unmasking_seq_len"]
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
            test_generator = UnmaskingTestGenerator(x_test, x_train, parameters)
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

        test_mask = numpy.random.choice([1,0], (len(x_test), test_generator.seq_len), p=[0.7,0.3])
        train_mask = numpy.random.choice([1,0], (len(x_train), test_generator.seq_len), p=[0.7,0.3])

        test_mask[:,-1] = 0
        train_mask[:,-1] = 0
        test_mask[:,0] = 1
        train_mask[:,0] = 1

        x_test_masked = x_test * test_mask
        x_train_masked = x_train * train_mask

        print("start embedding test data.")
        embedded_x_test = embedding_network.predict(x_test_masked)
        print("start embedding train data.")
        embedded_x_train = embedding_network.predict(x_train)
        print("done embedding.")

        top_1_rmse_min_average = []
        top_3_rmse_min_average = []
        top_5_rmse_min_average = []

        for i, sequence in enumerate(x_test_masked):

            y_mask = test_mask[i]
            y_true = x_test[i]

            test_embedded = embedded_x_test[i]
            distances = numpy.ravel(euclidean_distance([test_embedded, embedded_x_train]).numpy())
            lookup_indices = numpy.argsort(distances)
            top_1_indices = lookup_indices[:1]
            top_3_indices = lookup_indices[:3]
            top_5_indices = lookup_indices[:5]
            predictions_top_1 = x_train[top_1_indices]
            predictions_top_3 = x_train[top_3_indices]
            predictions_top_5 = x_train[top_5_indices]

            top_1_mask = train_mask[top_1_indices]
            top_3_mask = train_mask[top_3_indices]
            top_5_mask = train_mask[top_5_indices]
            combined_top_1_mask = 1 - (y_mask * top_1_mask) # invert it to exclude the non masked numbers afterwards
            combined_top_3_mask = 1 - (y_mask * top_3_mask)
            combined_top_5_mask = 1 - (y_mask * top_5_mask)


            # top_1_se = numpy.square(numpy.log(y_true + 1) - numpy.log(predictions_top_1 + 1)) # squared error
            # top_3_se = numpy.square(numpy.log(y_true + 1) - numpy.log(predictions_top_3 + 1))
            # top_5_se = numpy.square(numpy.log(y_true + 1) - numpy.log(predictions_top_5 + 1))

            top_1_se = numpy.square(y_true - predictions_top_1) # squared error
            top_3_se = numpy.square(y_true - predictions_top_3)
            top_5_se = numpy.square(y_true - predictions_top_5)

            top_1_se_cut = top_1_se * combined_top_1_mask
            top_3_se_cut = top_3_se * combined_top_3_mask
            top_5_se_cut = top_5_se * combined_top_5_mask

            top_1_averages = numpy.sqrt((1+numpy.sum(top_1_se_cut, axis=1)) / (numpy.count_nonzero(top_1_se_cut, axis=1)+0.1))
            top_3_averages = numpy.sqrt((1+numpy.sum(top_3_se_cut, axis=1)) / (numpy.count_nonzero(top_3_se_cut, axis=1)+0.1))
            top_5_averages = numpy.sqrt((1+numpy.sum(top_5_se_cut, axis=1)) / (numpy.count_nonzero(top_5_se_cut, axis=1)+0.1))

            top_1_min_rmse = numpy.min(top_1_averages)
            top_3_min_rmse = numpy.min(top_3_averages)
            top_5_min_rmse = numpy.min(top_5_averages)

            top_1_rmse_min_average.append(top_1_min_rmse)
            top_3_rmse_min_average.append(top_3_min_rmse)
            top_5_rmse_min_average.append(top_5_min_rmse)

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

class UnmaskingDataGenerator(tensorflow.keras.utils.Sequence):
    def __init__(self, x_all, y_all, parameters):
        self.seq_len = parameters["unmasking_seq_len"]
        self.batch_size = parameters["batch_size"]
        self.masks_per_batch = parameters["unmasking_masks_per_batch"]
        self.x_all = x_all[:,:self.seq_len]
        self.len = len(x_all)

    def __len__(self):
        return int(self.len / self.batch_size)

    def on_epoch_end(self):
        pass

    def __getitem__(self, index):

        begin = int(index*self.batch_size)
        end = int(begin + self.batch_size)

        unmasked_stack = self.x_all[begin:end]
        unmasked_stack = numpy.vstack([unmasked_stack]*self.masks_per_batch)
        masks = numpy.random.choice([1,0], (self.masks_per_batch, self.seq_len), p=[0.75,0.25])
        masks = numpy.repeat(masks, self.batch_size, axis=0)

        masked_stack = unmasked_stack * masks
        same_or_different_stack = numpy.count_nonzero(masks, axis=1) / self.seq_len

        return ([unmasked_stack, masked_stack], same_or_different_stack)

class UnmaskingTestGenerator():
    def __init__(self, x_test, x_train, parameters):
        self.seq_len = parameters["unmasking_seq_len"]
        self.x_test = x_test[:1000,:self.seq_len]
        self.x_train = x_train[:,:self.seq_len]
