# this is just a tester script for new implementations
import sys
import datetime
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["WANDB_SILENT"] = "true"
import models
import tasks
import tensorflow
import keras
import numpy


x_1 = numpy.array([
    [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [10,11,12,13,14,15,16,17,18,19],
    [20,21,22,23,24,25,26,27,28,29],
    [30,31,32,33,34,35,36,37,38,39],
    [40,41,42,43,44,45,46,47,48,49],
    [50,51,52,53,54,55,56,57,58,59],
    [60,61,62,63,64,65,66,67,68,69],
    [70,71,72,73,74,75,76,77,78,79],
    [80,81,82,83,84,85,86,87,88,89],
    [90,91,92,93,94,95,96,97,98,99],
])

x_2 = numpy.array([
    [1,2,3,4,5,6,7,8,9,3],
    [9,5,9,5,2,2,2,2,2,7],
    [3,2,7,7,7,7,7,7,7,1],
    [1,2,3,4,7,3,7,8,9,7],
    [3,2,4,6,3,2,5,8,4,7],
    [9,9,9,9,9,9,9,9,9,2],
])

y = numpy.array([
    [0,0,0,0],
    [0,0,0,1],
    [0,0,1,0],
    [0,0,1,1],
    [0,1,0,0],
    [0,1,0,1],
    [0,1,1,0],
    [0,1,1,1],
    [1,0,0,0],
    [1,0,0,1],    
])

parameters = {
    "batch_size": 2,
    "unmasking_seq_len": 10,
    "unmasking_masks_per_batch": 2
}

input_layer = keras.layers.Input(shape=(10,))
output_layer = keras.layers.Dense(units=2)(input_layer)
model = keras.models.Model(inputs=input_layer, outputs=output_layer)

data = tasks.UnmaskingTestGenerator(x_1, x_2, parameters)
a = tasks.Unmasking("","","","")
a.test(model, model, data, parameters, "oeis")