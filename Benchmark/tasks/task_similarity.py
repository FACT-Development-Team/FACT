from tasks import Task
from models import top_k_multiclass, euclidean_distance, contrastive_loss
import tensorflow
import keras
import numpy
import wandb
from wandb.keras import WandbCallback


class Similarity(Task):
    def __init__(self, model, category, category_name, time):
        super().__init__(model, category, category_name, time)
        self.name = "similarity"
        self.test_immediately = True

    def build_model(self, parameters, input_shape):
        input_layer_1 =  keras.layers.Input(name="input_1", shape=input_shape)
        input_layer_2 =  keras.layers.Input(name="input_2", shape=input_shape)

        parameters["last-layer_units"] = parameters["similarity_embedding_dim"] # embedding dim
        parameters["last-layer_activation"] = "sigmoid"

        embedding_network = self.model.build_model(parameters, input_shape) # dependent of the model task
        tower_1 = embedding_network(input_layer_1)
        tower_2 = embedding_network(input_layer_2)
        distance_layer = keras.layers.Lambda(name="distance", function=euclidean_distance)([tower_1, tower_2])

        model = keras.models.Model(name="continuation_task_"+self.model.name, inputs=[input_layer_1, input_layer_2], outputs=distance_layer)

        model.compile(optimizer="adam", loss=contrastive_loss(parameters["margin_distance"]))
        return (model, embedding_network)
        

    def get_train_data(self, dataset, parameters):
        x_train, y_train = dataset.get_train_data(category=self.category, encoding=parameters["encoding"])
        l_train = len(x_train)
        val_fraction = int(l_train*parameters["validation_split"])

        if l_train > 0:
            parameters["batch_size"] = int(max(32, l_train*0.001))
            train_generator = SimilarityDataGenerator(x_train[val_fraction:], y_train[val_fraction:], parameters)
            validation_generator = SimilarityDataGenerator(x_train[:val_fraction], y_train[:val_fraction], parameters)
        else:
            raise ValueError("training set cannot be empty.")

        input_shape = list(x_train.shape)
        input_shape[1] = parameters["similarity_seq_len"]
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
            test_generator = SimilarityTestGenerator(x_train, x_test, y_train, y_test, self.category, parameters)
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
        test_results = top_k_multiclass(optional_model, test_generator.x_train, test_generator.x_test, test_generator.y_train, test_generator.y_test, test_generator.category, verbose=True)
        if parameters["wandb"]:
            wandb.log(test_results)
        return test_results


class SimilarityDataGenerator(tensorflow.keras.utils.Sequence):
    def __init__(self, x_all, y_all, parameters):
        self.seq_len = parameters["similarity_seq_len"]
        self.x_all = x_all[:,:self.seq_len]
        self.y_all = y_all
        self.batch_size = parameters["batch_size"]
        self.parameters = parameters
        self.len = len(x_all)
        self.groups = [numpy.squeeze(numpy.argwhere(category)) for category in numpy.transpose(y_all)] # holds a list of indices from each category

    def __len__(self):
        return int(len(self.x_all) / self.batch_size)

    def on_epoch_end(self):
        pass

    def __getitem__(self, index):

        candidats = []
        # iterate over all groups/categories
        for group_id, group in enumerate(self.groups):

            # sample a fraction of the whole group f*sizeof(p_i), minimum 2, maximum 5 samples
            fraction = self.parameters["siamese_fraction"]
            samples = min(self.parameters["siamese_upper_limit"], max(self.parameters["siamese_lower_limit"], int(fraction*len(group))))
            members = numpy.random.choice(group, samples)
            
            for member in members:
                candidats.append((member, group_id))

        result = []
        # pairing all combinations of candidats
        for i, left in enumerate(candidats):
            for right in candidats[i+1:]:
                same_or_different = 1 if left[1] == right[1] else 0
                result.append([self.x_all[left[0]], self.x_all[right[0]], same_or_different])
        
        result = numpy.array(result, dtype=object)

        return ([numpy.stack(result[:,0]).astype(numpy.float32), numpy.stack(result[:,1]).astype(numpy.float32)], result[:,2].astype(numpy.float32))


class SimilarityTestGenerator():
    def __init__(self, x_train, x_test, y_train, y_test, category, parameters):
        self.seq_len = parameters["similarity_seq_len"]
        self.x_test = x_test[:1000,:self.seq_len]
        self.x_train = x_train[:,:self.seq_len]
        self.y_train = y_train
        self.y_test = y_test[:1000]
        self.category = category
