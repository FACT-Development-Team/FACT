# -----------------------------------------------------------
# Dataset wrapper for oeis and synthetic
# -----------------------------------------------------------

import numpy as np
import pandas as pd
import pickle
import os

class Dataset:
    def __init__(self, parameters, debug=False, sweep=False):

        self.parameters = parameters
        self.directory = os.path.join(parameters["directory"], "data")
        path = os.path.join(self.directory, "dataset")
        if debug:
            path += "_debug"
        path += ".pickle"

        pickle_in = open(path, "rb")
        self.data = pickle.load(pickle_in)
        pickle_in.close()

        self.seq_length = parameters["seq_length"]
        self.categories = [name for name in self.data.columns if "eval_" in name]
        self.sweep = sweep
        print(len(self.data), "datapoints loaded.")


    def get_train_data(self, category="eval_polynomial", encoding="text", n=None):
        """
        queries and encodes the dataset and returns a dataset-split tuple

        :param training_source: origin of the datapoints synthetic|oeis for training
        :param test_source: origin of the datapoints synthetic|oeis for testing
        :param category: binary classification category of the dataset
        :param encoding: encoding type of the data
        :param fraction: split ratio between test- and training-data
        :param n: limit, number of datapoints
        :return: (x_train, y_train, x_test, y_test)
        """  
        if type(category) == str:
            if category not in self.categories:
                raise ValueError(category, "category key not supported. Supported are:", self.categories)

            train_eval_true = self.data[self.data[category] == 1]
            train_eval_false = self.data[self.data[category] == 0]

            if len(train_eval_true) > len(train_eval_false):
                if n == None or n > len(train_eval_false):
                    n = len(train_eval_false)
            else:
                if n == None or n > len(train_eval_true):
                    n = len(train_eval_true)

            train_eval_true = train_eval_true.sample(n=n)
            train_eval_false = train_eval_false.sample(n=n)

            train_data = pd.concat([train_eval_true, train_eval_false], axis=0, ignore_index=True)

        elif isinstance(category, list):
            for c in category:
                if c not in self.categories:
                    raise ValueError(c, "category key not supported. Supported are:", self.categories)

            train_data = self.data

        else:
            raise ValueError("category should be a single category string or a categories list")

        if self.sweep:
            train_data = train_data.sample(frac=0.1).reset_index(drop=True)
        else:
            train_data = train_data.sample(frac=1).reset_index(drop=True)


        print("Train data:", len(train_data), "\n")

        x_train = self.encode(train_data["sequence"], encoding)
        y_train = train_data[category].to_numpy(dtype=np.float32)

        return (x_train, y_train)           
     
    def get_test_data(self, test_source, category="eval_polynomial", encoding="text", n=None):

        if test_source == "oeis":
            filename = "testset_oeis.pickle"
        elif test_source == "synthetic":
            filename = "testset_synth.pickle"
        else:
            raise ValueError("test-source not supported.")

        path = os.path.join(self.directory, filename)

        pickle_in = open(path, "rb")
        df = pickle.load(pickle_in)
        pickle_in.close()

        if type(category) == str:
            if category not in self.categories:
                raise ValueError(category, "category key not supported. Supported are:", self.categories)

            test_eval_true = df[df[category] == 1]
            test_eval_false = df[df[category] == 0]

            if len(test_eval_true) > len(test_eval_false):
                if n == None or n > len(test_eval_false):
                    n = len(test_eval_false)
            else:
                if n == None or n > len(test_eval_true):
                    n = len(test_eval_true)

            test_eval_true = test_eval_true.sample(n=n)
            test_eval_false = test_eval_false.sample(n=n)

            test_data = pd.concat([test_eval_true, test_eval_false], axis=0, ignore_index=True)

        elif isinstance(category, list):
            for c in category:
                if c not in self.categories:
                    raise ValueError(c, "category key not supported. Supported are:", self.categories)

            test_data = df

        else:
            raise ValueError("category should be a single category string or a categories list")

        if self.sweep:
            test_data = test_data.sample(frac=0.1).reset_index(drop=True)
        else:
            test_data = test_data.sample(frac=1).reset_index(drop=True)


        print("Test data:", len(test_data), "\n")

        x_test = self.encode(test_data["sequence"], encoding)
        y_test = test_data[category].to_numpy(dtype=np.float32)

        return (x_test, y_test)  


    def encode(self, pd_series, encoding):
        """
        encodes a series

        :param pd_series: pandas series of sequences
        :param encoding: encoding method
        :return: encoded numpy 2d-array
        """   
        if encoding == "text":
            VOCABULARY = {
                "0": 0, "1": 1, "2": 2, "3": 3, "4": 4,
                "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
                ",": 0, "-": 0, "[": 0, "]": 0
            }
            return np.array([[VOCABULARY[i] for i in s[:self.seq_length]] for s in pd_series.to_numpy()])

        elif encoding == "dense":
            def split_and_pad(sequence):
                return [list(s.zfill(12))[:12] for s in sequence.split(",")]
            a = np.array(pd_series.apply(split_and_pad).tolist())
            a[a == "-"] = "0"
            a = a.astype(self.datatype)
            return a

        elif encoding == "raw":
            return np.array([s.split(",") for s in pd_series.to_numpy()], np.int64)
        else:
            raise ValueError("wrong encoding parameter.")

