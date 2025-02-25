# Benchmarkign Setup Documentation
This piece of documentation describes how our benchmark can be used to reproduce our results shown in the corresponding paper.


## License
This work is licensed under the Creative Commons Attribution 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

## Experiment
The benchmark is composed of a number of experiments.
An experiment is a specific model architecture, trained on a specific task, within a category or across all of them -- in other words, it's a triple (architecture, task, data span).
A detailed explanation on how to launch an experiment is given in the section **Training a model**.
Wherever possible, the default random seed is 1234.

## Workspace Initialization
1. Download the already-preprocessed, stripped-down, and split FACT dataset from the [ETH Research Collection (DOI 10.3929/ethz-b-000562705)](https://doi.org/10.3929/ethz-b-000562705) to your local machine. This requires about 1 GB of space, and there is a separate README for the archive. In short, size ratios between training, validation, synthetic testing, and OEIS testing datasets are 9:1:1:1.
2. Create a local directory called `local` (or any other name). This will be the directory where all of the experimental data will be stored.
3. Create two subfolders called `local/data` and `local/trained_models`. The former will store the training data while the latter will hold model checkpoints.
4. Make sure that your `local` directory has enough space to store all your experiments. One experiment can require up to 1-2 GB of space.
5. Move dataset pickle files (`dataset.pickle`, `dataset_debug.pickle, testset_oeis.pickle, testset_synth.pickle`) into your `local/data` folder.
6. Separately, clone the FACT repository from github with `git clone git@github.com:FACT-Development-Team/FACT.git`. The target directory of the clone is not important, but it may perhaps be better to keep it separate from `local`.
7. Open `FACT/Benchmark/parameters/parameter.py` and change the directory on line 2 to the **absolute** path of your local directory. Preserve the `os.path` call argument structure so that your path remains OS-agnostic.
8. Open a terminal equipped with a Python installation, enter `FACT/Benchmark`, and execute `pip install -r requirements.txt`.
9. You can now run any experiment you wish as per the next section.

## Training a Model

To start a new experiment, execute `train.py` with the required parameters.

**Syntax:**

```python
python3 train.py <task> <architecture> <category>
```

You can specify **multiple** values for \<task\>, \<architecture\>, and \<category\> at once. The experiments will be executed in a grid format over all values.


### Supported Parameters:

**`<task>`**

| Value             | Description |
| -------------- | ------- |
| classification | (default value) Classifies the input sequence to one or more categories (multiclass). |
| similarity | Embeds two sequences so that similar ones, such as those from the same category or sharing similar properties, are positioned closer in the embedding space than unrelated sequences. |
| next | Given two contiguous sub-sequences s1 and s2, the objective of the next sequence-part prediction task is to determine whether the sub-sequence s2 is a valid continuation of s1. |
| continuation | Suggest the next entry of a given sequence (single-shot). |
| generation | Suggest the next **n** entries of a given sequence (multi-shot). |
| unmasking | Unmask **n** randomly selected masked entries in a given sequence. |

**`<architecture>`**

| Value             | Description | Implementation |
| --- | --- | --- |
| Dense | Multi-Layer Perceptron | `models/model_dense.py` |
| RNN | Long Short-Term Memory | `models/model_rnn.py` |
| CNN | Convolutional Neural Network | `models/model_cnn.py` |
| Transformer | Self-Attention Transformer Encoder | `models/model_transformer.py` |
| KNNC | K-Nearest-Neighbors-Classifier | Scikit-learn: `KNeighborsClassifier` |
| GNBC | Gaussian-Naive-Bayes-Classifier | Scikit-learn: `GaussianNB` |
| LSVC | Linear-Support-Vector-Machine-Classifier | Scikit-learn: `LinearSVC` |
| DTC | Decision-Tree-Classifier | Scikit-learn: `DecisionTreeClassifier` |
| RFC | Random-Forest-Classifier | Scikit-learn: `RandomForestClassifier` |
| GBC | Gradient-Boosting-Classifier | Scikit-learn: `GradientBoostingClassifier` |

**`<category>`**

`polynomial, exponential, trigonometric, periodic, finite, modulo, prime, bounded, increasing, unique, all (default)`

**Examples:**
```python
python3 train.py similarity RNN polynomial
```
Training a recurrent neural-network on the similarity task within the polynomial category. This will launch **1** experiment.

```python
python3 train.py classification CNN,RFC finite,modulo
```
Training a convolutional neural-network, decision-tree and a random-forest-classifier on the classification task within the finite, modulo and prime categories. This will launch **9** experiments.


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