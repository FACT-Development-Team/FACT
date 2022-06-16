import sys
import datetime
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["WANDB_SILENT"] = "true"
import wandb
from experiments import Experiment
from dataset import Dataset
from parameters import parameters

dataset = Dataset(debug=parameters["debug"], parameters=parameters)

tasks = ["classification", "similarity", "next", "continuation", "generation", "unmasking"]
models = [
    "Dense", "RNN", "Transformer", "CNN",
    "KNNC", "GNBC", "LSVC", "DTC", "RFC", "GBC", "ABC", "XGBC", "DYC",
    "KNNR", "LIR", "RIR", "LAR", "ENR", "DTR", "RFR", "GBR", "ABR", "XGBR", "DYR"
    ]
categories = ["polynomial", "exponential", "trigonometric", "periodic", "finite", "modulo", "prime", "bounded", "increasing", "unique", "all"]

try:
    arguments = sys.argv[1].split(",")
    if all(x in tasks for x in arguments):
        tasks = arguments
    else:
        raise ValueError(arguments, "task not supported")
except IndexError:
    tasks = ["classification"]
try:
    arguments = sys.argv[2].split(",")
    if all(x in models for x in arguments):
        models = arguments
    else:
        raise ValueError(arguments, "model not supported")
except IndexError:
    models = ["Dense", "RNN", "Transformer", "CNN"]
try:
    arguments = sys.argv[3].split(",")
    if all(x in categories for x in arguments):
        categories = arguments
    else:
        raise ValueError(arguments, "category not supported")
except IndexError:
    pass


for task in tasks:
    for model in models:
        for category in categories:

            time = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
            if parameters["wandb"]:
                wandb.init(project="exp_"+task, entity="flavioschenker", group=model, name=category + "_" + time, allow_val_change=True)

            epx = Experiment(dataset, parameters, task, model, category, time)
            epx.run()

            if parameters["wandb"]:
                wandb.finish()


# restricitions:
# models KNNC, GNBC,... only works in classification and all categories except all
# task_similarity only works for category=all
# task_continuation only works for encoding=raw
# trigonometric evaluation in oeis not possible, oeis has no trigonometric entities