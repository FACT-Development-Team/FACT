# OEIS Processing

## License
Copyright 2022 FACT Development Team under ETHZ TIK DISCO

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Annotator

In order to use the annotator, we assume that the OEIS dataset has already been downloaded.
You can find the downloaded dataset stored with the [ETH Research Collection](https://doi.org/10.3929/ethz-b-000562705), or, alternatively, [here](https://1drv.ms/u/s!Ah0yjm0w0EzPuJJdflcIGeBR5zLJkg).

### Quick Run

1. Open a terminal equipped with a Python installation, enter `FACT/OEIS Processing`, and execute `pip install -r requirements.txt`.
2. Store the dataset in this subrepo (i.e. under FACT/OEIS Processing) and run
```
python3 Annotator/example_implementation.py
```
3. You should see dummy annotations stored in the repo under the names: `combined_results.csv` and `overview.csv`.

### Annotator interface
A quick example how annotator is used can be found here (pseudocode):
```
def main():
    my_list_of_classification_methods = [classification_method, classification_method_2, classification_method_3]

    my_Anotator = Anotator("my_example_category", my_list_of_classification_methods, aggregator)
    my_Anotator.run_and_save()
```
The Aggregator should return a single integer in the range [0,4] as described in the main paper.
The function "run_and_save" runs all classification methods on every sequence and saves the results from the aggregator in the files:
```
combined_results.csv
overview.csv
```
which are created when they do not already exist in the directory.

### Classification methods
As you can see in the previous example the user should specify `classification_method()` and use it in conjuction with Annotator.
An example for a classification can be:
```
def classification_method(data_dict):
    my_words = ["bli", "BLA", "blu"]
    return basic_word_search(data_dict, my_words, "comments", case_sensitve = True)
```
The above method checks whether the sequences contains the word bli, BLA or blu in comments column of the dataset.

#### Classification methods - detailed
Classification Methods can acccess the fields of the dataset via the dictionary "data_dict" by using the column names:
```python
            column_names = [
                "oeis_id",
                "identification",
                "value_list",
                "name",
                "comments",
                "detailed_references",
                "links",
                "formulas",
                "examples",
                "maple_programs",
                "mathematica_programs",
                "other_programs",
                "cross_references",
                "keywords",
                "offset_a",
                "offset_b",
                "author",
                "extensions_and_errors"]
```
For example the field "name" can be accessed via data_dict["name"]. Be careful to test for existance of every field you access. For example:
```python
            if data_dict["name"] is not None:
                #use data_dict["name"] here.
            else:
                #do not use data_dict["name"] here.
```
Classification Methods can return whatever desired. The aggregator receives a list that contains one entry per classification method. (i.e. what the aggreagtor receives as an input is:
```python
            result = [whatever_was_returned_from_classification_method_1,
                      whatever_was_returned_from_classification_method_2,
                      whatever_was_returned_from_classification_method_3,
                      ...
                      ]
            )
```
