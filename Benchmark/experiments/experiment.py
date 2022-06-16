import models
import tensorflow as tf
import tasks
import pickle
import keras
import os
from models import f1_multiclass_metric, top_k_multiclass, euclidean_distance, contrastive_loss

class Experiment:
    def __init__(self, dataset, parameters, task, model, category, time):

        self.time = time
        self.dataset = dataset
        self.parameters = parameters
        self.has_optional_model = False
        self.categories = ["polynomial", "exponential", "trigonometric", "periodic", "finite", "modulo", "prime", "bounded", "increasing", "unique", "all"]

        if category in self.categories:
            if category == "all":
                self.category = self.categories
                self.category_name = "all"
                self.category.remove("all")
                self.category = ["eval_" + c for c in self.category]
            else:
                self.category = "eval_" + category
                self.category_name = category
        else:
            raise ValueError("category", category, "not supported.")
        

        if model == "Dense":
            self.model = models.Dense()
        elif model == "RNN":
            self.model = models.RNN()
        elif model == "Transformer":
            self.model = models.Transformer()
        elif model == "CNN":
            self.model = models.CNN()
        elif model == "KNNC" and task == "classification":
            self.model = models.KNNC()
        elif model == "GNBC" and task == "classification":
            self.model = models.GNBC()
        elif model == "LSVC" and task == "classification":
            self.model = models.LSVC()
        elif model == "DTC" and task == "classification":
            self.model = models.DTC()
        elif model == "RFC" and task == "classification":
            self.model = models.RFC()
        elif model == "GBC" and task == "classification":
            self.model = models.GBC()
        elif model == "ABC" and task == "classification":
            self.model = models.ABC()
        elif model == "XGBC" and task == "classification":
            self.model = models.XGBC()
        elif model == "DYC" and task == "classification":
            self.model = models.DYC()
        elif model == "KNNR" and task == "continuation":
            self.model = models.KNNR()
        elif model == "LIR" and task == "continuation":
            self.model = models.LIR()
        elif model == "RIR" and task == "continuation":
            self.model = models.RIR()
        elif model == "LAR" and task == "continuation":
            self.model = models.LAR()
        elif model == "ENR" and task == "continuation":
            self.model = models.ENR()
        elif model == "DTR" and task == "continuation":
            self.model = models.DTR()
        elif model == "RFR" and task == "continuation":
            self.model = models.RFR()
        elif model == "GBR" and task == "continuation":
            self.model = models.GBR()
        elif model == "ABR" and task == "continuation":
            self.model = models.ABR()
        elif model == "XGBR" and task == "continuation":
            self.model = models.XGBR()
        elif model == "DYR" and task == "continuation":
            self.model = models.DYR()
        else:
            raise ValueError("model", model, "not supported for this task", task, " or in general.")


        if task == "classification":
            self.task = tasks.Classification(self.model, self.category, self.category_name, self.time)
        elif task == "next":
            self.task = tasks.Next(self.model, self.category, self.category_name, self.time)
        elif task == "similarity":
            self.task = tasks.Similarity(self.model, self.category, self.category_name, self.time)
        elif task == "generation":
            self.task = tasks.Generation(self.model, self.category, self.category_name, self.time)
        elif task == "continuation":
            self.task = tasks.Continuation(self.model, self.category, self.category_name, self.time)
        elif task == "unmasking":
            self.task = tasks.Unmasking(self.model, self.category, self.category_name, self.time)
        else:
            raise ValueError("task", task, "not supported.")

        print("\n|| New Experiment || task:", self.task.name, ", model:", self.model.name, ", category:", self.category_name, "||")

    def run(self):

        train_generator, input_shape = self.task.get_train_data(self.dataset, self.parameters)
        model, optional_model = self.task.build_model(self.parameters, input_shape[1:])
        if self.model.dependency == "Keras":
            model.summary()
            if optional_model is not None:
                self.has_optional_model = True
                optional_model.summary()
        elif self.model.dependency == "Sklearn":
            pass
        else:
            raise ValueError("dependency not supported.")
        trained_model = self.task.train(model, train_generator, self.parameters)
        self.save(trained_model, optional_model)

        if(self.parameters["test_immediately"] and self.task.test_immediately):
            self.test_immediately(model, optional_model, "oeis")
            self.test_immediately(model, optional_model, "synthetic")
        else:
            print("no immediate evaluation.")

    def save(self, model, optional_model):
        directory = self.parameters["directory"]

        filename = "trained_models/" + self.task.name + "/" + self.model.name + "/" + self.category_name + "/" + self.time + "_experiment.pickle"
        path = os.path.join(directory, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        pickle_out = open(path, "wb")
        pickle.dump(self, pickle_out)
        pickle_out.close()

        if self.model.dependency == "Keras":
            filename = "trained_models/" + self.task.name + "/" + self.model.name + "/" + self.category_name + "/" + self.time + "_model"
            path = os.path.join(directory, filename)
            model.save(path)
            if self.has_optional_model:
                filename = "trained_models/" + self.task.name + "/" + self.model.name + "/" + self.category_name + "/" + self.time + "_optional_model"
                path = os.path.join(directory, filename)
                optional_model.save(path) 

        elif self.model.dependency == "Sklearn":
            filename = "trained_models/" + self.task.name + "/" + self.model.name + "/" + self.category_name + "/" + self.time + "_model.pickle"
            path = os.path.join(directory, filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            pickle_out = open(path, "wb")
            pickle.dump(model, pickle_out)
            pickle_out.close()
        else:
            raise ValueError("dependency not supported.")

    def test(self, test_source):
        from keras import backend as kb
        print("\n|| New Evaluation || test_source:", test_source, "task:", self.task.name, ", model:", self.model.name, ", category:", self.category_name, "||")

        directory = self.parameters["directory"]
        if self.model.dependency == "Keras":
            filename = "trained_models/" + self.task.name + "/" + self.model.name + "/" + self.category_name + "/" + self.time + "_model"
            path = os.path.join(directory, filename)
            model = keras.models.load_model(path, custom_objects={"tf": tf})
            if self.has_optional_model:
                filename = "trained_models/" + self.task.name + "/" + self.model.name + "/" + self.category_name + "/" + self.time + "_optional_model"
                path = os.path.join(directory, filename)
                optional_model = keras.models.load_model(path, compile=False)
            else:
                optional_model = None

        elif self.model.dependency == "Sklearn":
            filename = "trained_models/" + self.task.name + "/" + self.model.name + "/" + self.category_name + "/" + self.time + "_model.pickle"
            path = os.path.join(directory, filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            pickle_in = open(path, "rb")
            model = pickle.load(pickle_in)
            pickle_in.close()
        else:
            raise ValueError("dependency not supported.")

        test_generator = self.task.get_test_data(test_source, self.dataset, self.parameters)

        if test_generator is not None:
            test_result = self.task.test(model, optional_model, test_generator, self.parameters, test_source)
            print("Evaluation done.")
            print(test_result)
        else:
            print("skipping evaluation, no test data available.")


    def test_immediately(self, model, optional_model, test_source):

        print("\n|| New Evaluation || test_source:", test_source, "task:", self.task.name, ", model:", self.model.name, ", category:", self.category_name, "||")

        test_generator = self.task.get_test_data(test_source, self.dataset, self.parameters)

        if test_generator is not None:
            test_result = self.task.test(model, optional_model, test_generator, self.parameters, test_source)
            print("Evaluation done.")
            print(test_result)
        else:
            print("skipping evaluation, no test data available.")