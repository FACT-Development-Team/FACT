# FACT
Learning Governing Abstractions Behind Integer Sequences

Integer sequences are of central importance to the modeling of concepts admitting complete finitary descriptions. We introduce a novel view on the learning of such concepts and lay down a set of benchmarking tasks aimed at conceptual understanding by machine learning models. These tasks indirectly assess model ability to abstract, and challenge them to reason both interpolatively and extrapolatively from the knowledge gained by observing representative examples. To further aid research in knowledge representation and reasoning, we present FACT, the Finitary Abstraction Comprehension Toolkit. The toolkit surrounds a large dataset of integer sequences comprising both organic and synthetic entries, a library for data pre-processing and generation, a set of model performance evaluation tools, and a collection of baseline model implementations, enabling the making of the future advancements with ease.


This repository consists of the OEIS processing code, FACTLIB, and the Benchmarking Setup. Each is described below in more detail.

## Accessing the Dataset
The main FACT dataset is available as a SQLite database with the ETH Research Collection. You can use any SQLite library to make the connection from your code to the dataset.

[DOI 10.3929/ethz-b-000562705](https://doi.org/10.3929/ethz-b-000562705)

To quickly inspect the dataset, tools such as [DB Browser (SQLite)](https://sqlitebrowser.org/) might come handy.
There is a `UNIQUE INDEX` on the `oeis_id` column to speed up listing and ID lookups. If you plan to search the dataset through a different column, consider indexing it to improve performance.

Additionally, there is also a sub-dataset created specifically for our benchmark that contains no NLP annotations or other additional information that is solicited for OEIS entries.
This file is significantly smaller and contains: the `oeis_id`s uniquely identifying each sequence, the `sequence` itself, and some flag (`1` or `0`) fields marking whether the sequence is `trigonometric`, `polynomial`, `exponential`, etc.. It is also a part of the above repository held by the ETH Research Collection.

More information can be found in the README distributed with the version of the dataset.

### QuickStart Guide

You will find a QuickStart Jupyter Notebook file under `./QuickStart`. `pytorch` and `torchvision` are its two notable requirements.

### OEIS Processing
You will find all code and more information about the processing steps for OEIS data that was included into the FACT dataset under `./OEIS Processing`.
We recommend starting with the `README.md` file in that directory.

### FACTLIB
A library for generation of synthetic sequences, available under `./FACTLIB`.
Individual generation sub-modules and functions, main ones documented with docstrings, can then be invoked directly or used as ready-made snippets as in `main.py`.

The version found in this repository is the most recent one.
The initial version, coupled with the paper, can be found under [DOI 10.3929/ethz-b-000565638](https://doi.org/10.3929/ethz-b-000565638).

### Benchmarking Setup
A benchmarking setup with a range of models and tasks as well as apropriate evaluation metrics.

The version found in this repository is the most recent one.
The initial version, coupled with the paper, can be found under [DOI 10.3929/ethz-b-000565644](https://doi.org/10.3929/ethz-b-000565644).

## Contact and Acknowledgements
Feel free to contact <akastrati@ethz.ch> and <belcak@ethz.ch> in case you have any questions.
 * Peter Belcak (maintainer)
 * Emanual Jampen (OEIS data processing)
 * Ard Kastrati (maintainer, OEIS data processing, synthetic sequence generation)
 * Flavio Schenker (baseline model implementation)
 * Neil Sloane (the author and maintainer of The Online Encyclopedia of Integer Sequences <https://oeis.org/>)

 ## Licenses

 ### OEIS
 This work is licensed under the Creative Commons Attribution-NonCommercial 3.0 Unported License.
 To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/3.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

 ### FACT Dataset
 This work is licensed under the Creative Commons Attribution-NonCommercial 3.0 Unported License.
 To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/3.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

 ### FACT Benchmarking and FACTLIB
 This work is licensed under the Creative Commons Attribution 4.0 International License.
 To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
