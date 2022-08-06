# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 08:40:37 2021

"""


from anotator import Anotator
from anotator import basic_word_search


"""
    Classification Methods can acccess the fields of the dataset via the
        dictionary "data_dict" by using the column names:
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
        for example the field "name" can be accessed via data_dict["name"].
        Be careful to test for existance of every field you access.
        For example:
            if data_dict["name"] is not None:
                #use data_dict["name"] here.
            else:
                #do not use data_dict["name"] here.

    Classification Methods can return whatever desired. The aggregator
        receives a list that contains one entry per classification method.
        (i.e. what the aggreagtor receives as an input is:
            result = [whatever_was_returned_from_classification_method_1,
                      whatever_was_returned_from_classification_method_2,
                      whatever_was_returned_from_classification_method_3,
                      ...
                      ]
        )


    The Aggregator should return a single integer in the range [0,4] as described
        in the report.

    The function "basic_word_search" can be used to check if any one of a list
        of strings is found in one specific dataset field.
        If a match is found, the function returns 1.
        If the field is None the function returns 4.
        Else the function returns 0.
        See classification_method_3 for an example.

    The function "run_and_save" runs all classification methods on every sequence
        and saves the results from the aggregator in the files:
            combined_results.csv
            overview.csv
        which are created when they do not already exist in the directory.

"""




def classification_method_1(data_dict):
    if data_dict["name"] is not None:
        if len(data_dict["name"]) > 21:
            return 0
        else:
            return 1


def classification_method_2(data_dict):
    if data_dict["value_list"] is not None:
        values = data_dict["value_list"]
        if len(values) > 0:
            average_value = sum(values)/len(values)
            if average_value > 10:
                return 1
            else:
                return 2
        else:
            return 0
    return 4


def classification_method_3(data_dict):
    my_words = ["bli", "BLA", "blu"]
    return basic_word_search(data_dict, my_words, "comments", case_sensitve = True)

def aggregator(results):
    if results[0] == 1 and results[1] == 2:
        return 3
    if results[2] == 1:
        return 2
    return 0

def main():

    my_list_of_classification_methods = [classification_method_1, classification_method_2, classification_method_3]

    my_Anotator = Anotator("my_example_category", my_list_of_classification_methods, aggregator)
    my_Anotator.run_and_save()
