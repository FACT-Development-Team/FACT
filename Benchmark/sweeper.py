import sys
import datetime
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["WANDB_SILENT"] = "true"
import wandb
from experiments import Experiment
from dataset import Dataset
from parameters import parameters, get_hyperparameters, hyperparameters_Dense, hyperparameters_RNN, hyperparameters_Transformer, hyperparameters_CNN

dataset = Dataset(seq_length=parameters["seq_length"], datatype=parameters["datatype"], debug=parameters["debug"], sweep=True)

tasks = ["classification", "similarity", "next"]
models = ["Dense", "RNN", "Transformer", "CNN"]
categories = ["polynomial", "exponential", "trigonometric", "all"]


try:
    arguments = sys.argv[1].split(",")
    if all(x in tasks for x in arguments):
        tasks = arguments
    else:
        print(arguments, "task not supported")
except:
    pass
try:
    arguments = sys.argv[2].split(",")
    if all(x in models for x in arguments):
        models = arguments
    else:
        print(arguments, "task not supported")
except:
    pass
try:
    arguments = sys.argv[3].split(",")
    if all(x in categories for x in arguments):
        categories = arguments
    else:
        print(arguments, "task not supported")
except:
    pass


def run(experiment, model, category, time):
    def train():
        wandb.init(name=model + "_" + category + "_" + time, allow_val_change=True)
        config = wandb.config
        experiment.run(config)
    return train

for task in tasks:
    for model in models:
        for category in categories:

            time = datetime.datetime.now().strftime("%d-%m-%y_%H:%M:%S")
            hyperparameters = get_hyperparameters(parameters, hyperparameters_CNN)

            sweep_id = wandb.sweep(hyperparameters, project="sweep_"+task+"_"+model)
            exp = Experiment(dataset, task, model, "synthetic", category, time)
            wandb.agent(sweep_id=sweep_id, function=run(exp, model, category, time))


