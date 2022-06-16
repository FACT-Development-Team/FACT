import pickle
import os

class Task():
    def __init__(self, model, category, category_name, time):
        self.model = model
        self.category = category
        self.category_name = category_name
        self.time = time
        self.test_immediately = False

    def build_model(self, parameters, input_shape):
        raise NotImplementedError("this task should implement a build_model method.")

    def get_train_data(self, *parameters):
        raise NotImplementedError("this task should implement a get method.")

    def get_test_data(self, *parameters):
        raise NotImplementedError("this task should implement a get method.")

    def train(self, *parameters):
        raise NotImplementedError("this task should implement a train method.")

    def test(self, *parameters):
        raise NotImplementedError("this task should implement a test method.")

