# Benchmarkign Setup Documentation
This piece of documentation describes how our benchmark can be used to reproduce our results shown in the corresponding paper.

## Experiment
The benchmark is composed of a number of experiments.
An experiment is a specific model architecture, trained on a specific task, within a category or across all of them -- in other words, it's a triple (architecture, task, data span).
A detailed explanation on how to launch an experiment is given in the section **Training a model**.

## Workspace Initialization
1. Download the already preprocessed datasets from [Polybox](https://polybox.ethz.ch/index.php/s/sV5v8zeDZm6ArTd) to your local machine. This requires about 1 GB of space, and there is a separate README for the archive.
2. Create a local directory called `local` (or any other name). This will be the directory where all of the experimental data will be stored.
3. Create two subfolders called `local/data` and `local/trained_models`. The former will store the training data while the latter will hold model checkpoints.
4. Make sure that your `local` directory has enough space to store all your experiments. One experiment can require up to 1-2 GB of space.
5. Move dataset pickle files (`dataset.pickle`, `dataset_debug.pickle, testset_oeis.pickle, testset_synth.pickle`) into your `local/data` folder.
6. Separately, clone the FACT repository from github with `git clone git@github.com:FACT-Development-Team/FACT.git`. The target directory of the clone is not important, but it may perhaps be better to keep it separate from `local`.
7. Open `FACT/Benchmark/parameters/parameter.py` and change the directory on line 2 to the **absolute** path of your local directory. Preserve the `os.path` call argument structure so that your path remains OS-agnostic.
8. Open a terminal equipped with a Python installation, enter `FACT/Benchmark`, and execute `pip install -r requirements.txt`.
9. You can now run any experiment you wish as per the next section.

## Training a Model

You can launch a new experiment by executing `train.py`.

The script needs to be launched directly in a terminal with the necessary parameters. Syntax:
```python
python3 train.py <task> <model-architecture> <category>
```

Running multiple tasks, model-architectures, and categories per instance **is supported**. The resulting experiments will be run in grid mode from left to right.

Default parameters:
* \<task\> = `classification`
* \<model-architecture\> = `Dense,RNN,Transformer,CNN`
* \<category\> = all 10 supported categories and across all

Supported parameters:
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
3. Training models for all experiments at once.

    command:
    ```python
    python3 train.py
    ```
    This will launch **1x4x11=44!** experiments.

## Testing a Model

After you have sucessfully trained an experiment and stored the trained model to disk, you can test it with `test.py`.

Syntax:
```python
python3 test.py <task>/<model-architecture>/<category>/<date>
```
### Example:
I want to test my experiment, which was a classification task, trained with a Dense model within the polynomial category. The experiment was launched on 01.01.2022 at 15:30:00.

command:
```python
python3 test.py classification/Dense/polynomial/01-01-22_15-30-00
```
### Immediate Testing
Some tasks support immediate testing of your trained model and will print the evaluation on the test-set right after training. To do this, activate the `test_immediately` parameter in `parameter.py`
