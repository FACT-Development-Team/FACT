import sys
import datetime
import os
import pickle
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["WANDB_SILENT"] = "true"
import wandb
from experiments import Experiment
from dataset import Dataset
from parameters import parameters


test_sources = ["synthetic", "oeis"]

try:
    filename = sys.argv[1] + "_experiment.pickle"
    directory = parameters["directory"] + "/trained_models"
    path = os.path.join(directory, filename)
    pickle_in = open(path, "rb")
    experiment = pickle.load(pickle_in)
    pickle_in.close()
except IndexError:
    raise ValueError("no test model specified.")

try:
    arguments = sys.argv[2].split(",")
    if all(x in test_sources for x in arguments):
        test_sources = arguments
    else:
        raise ValueError(arguments, "test_source not supported.")
except IndexError:
    pass

for test_source in test_sources:
    if parameters["wandb"]:
        wandb.init(project="exp_"+experiment.task.name, entity="flavioschenker", group=experiment.model.name, name="evaluation of "+experiment.time)
    experiment.test(test_source)