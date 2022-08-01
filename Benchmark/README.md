# Benchmark documentation
This documentation describes how our benchmark can be used to reproduce our results shown in the corresponding paper.
## Experiment
The benchmark is composed of many experiments. An experiment is a specific model architecture, trained on a specific task, within a category.
A detailed explanation on how to launch an experiment is given in the section **"Training a model"**.

## Initialize Workspace
1. download the datasets from [Polybox](https://polybox.ethz.ch/index.php/s/3U2aJrRNQCOWit9) to your local machine. This requires about 1 GB of space.
2. create a local directory called `local` (or any other name).
3. create two subfolders called `local/data` and `local/trained_models`
4. make sure that your local directory has enough space to store your experiments. One experiment can require up to 1-2 GB of space.
5. move the dataset file into your `local/data` folder. `local/data/dataset.pickle`
6. repeat 5. with the other datasets. `dataset_debug.pickle, testset_oeis.pickle, testset_synth.pickle`
6. clone the FACT repository from github with `git clone git@github.com:FACT-Development-Team/FACT.git`.
7. open the `FACT/Benchmark/parameters/parameter.py` script.
8. change the directory on line 2 to the **absolute** path of your local directory. Preserve the os.path structure, such that you can use it on any operating system.
9. open a python configured terminal and `cd FACT/Benchmark` into the benchmark folder. From there you can run any experiment.

## Training a model

You can launch a new experiment with the `train.py` script.

The script should be launched directly in a terminal with the necessary parameters. Syntax:
```python
python3 train.py <task> <model-architecture> <category>
```

Running multiple tasks, model-architectures and categories per instance **is supported**. The resulting experiments will be run in grid mode from left to right.

default parameters:
* \<task\> = `classification`
* \<model-architecture\> = `Dense,RNN,Transformer,CNN`
* \<category\> = all 10 supported categories and across all

supported parameters:
* \<task\> = `classification,similarity,next,continuation,generation,unmasking`
* \<model-architecture\> = `Dense,RNN,Transformer,CNN`
* \<category\> = `polynomial,exponential,trigonometric,periodic,finite,modulo,prime,bounded,increasing,unique,all`

### Example:
1. Training a recurrent neural-network on the similarity task within the polynomial category.

    command:
    ```python
    python3 train.py similarity RNN polynomial
    ```
    This will launch **one** experiment.
2. Training a convolutional neural-network and a random-forest classifier on the classification task within the finite and modulo categories.

    command:
    ```python
    python3 train.py classification CNN,RFC finite,modulo
    ```
    This will launch **four** experiments.
3. Using the standard parameters.

    command:
    ```python
    python3 train.py
    ```
    This will launch **1x4x11=44!** experiments.

## Testing a model

After you have sucessfully launched an experiment and stored the trained model to disk, you can test it with `test.py`.

Syntax:
```python
python3 test.py <task>/<model-architecture>/<category>/<date>
```
### Example:
I want to test my experiment, which was a classification-task, trained on a Dense-model within the polynomial category. The experiment was launched on 01.01.2022 15:30:00.

command:
```python
python3 test.py classification/Dense/polynomial/01-01-22_15-30-00
```
### Immediate Testing
Some tasks support immediate testing of your trained model and will print the evaluation on the test-set right after training. To do this, activate the `test_immediately` parameter in `parameter.py`
