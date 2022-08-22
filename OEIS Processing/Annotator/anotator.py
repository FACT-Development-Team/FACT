# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:49:35 2021
This file contains the functions that are used to annotate the database.
See individual docstrings for more details.
"""

import numpy as np
import sqlite3
from numpy import savetxt
import types

class Error(Exception):
    """Base class for other exceptions"""

class InvalidNameError(Error):
    """raised when the category_name contains "# " or "\n" or " ". """

class Anotator():
    def __init__(self, category_name, tests, aggregator, database_size=342305):
        if "# " in category_name or "\n" in category_name or " " in category_name:
            print("do not use \"# \" or \"\\n\" or \" \" in the category name")
            raise InvalidNameError

        self.database_size = database_size
        self.anotations = np.zeros(self.database_size)
        self.category_name = category_name
        self.aggregator = aggregator
        self.file_name_results = "combined_results.csv"
        self.file_name_overview = "overview.csv"



        if type(tests) == list:
            self.tests = tests
        elif type(tests) == types.FunctionType:
            self.tests = [tests]
        else:
            print("provide tests either as a list of functions or as a single function")

    def run_and_save(self):
        self.anotate_all_sequences()
        self.save_anotations_to_file()
        self.save_to_overview()

    def __create_cursor(self):
        connection = sqlite3.connect('oeis_parsed.sqlite3')
        sql_cursor = connection.cursor()
        return sql_cursor

    def __get_data_row_as_dict(self, sql_cursor, oeis_id):
        sql_cursor.execute('''SELECT * FROM oeis_entries WHERE oeis_id = ?''',(str(oeis_id),))
        data_row = sql_cursor.fetchone()

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

        data_dict = {}

        for i in range(len(column_names)):
            data_dict[column_names[i]] = data_row[i]

        if data_row[2] and data_row[2] != "":
            data_dict["value_list"] = np.asarray(list(map(int, data_row[2].split(','))),dtype = "object")
        else:
            data_dict["value_list"] = None

        return data_dict

    #add new tests to the anotator, either as a list of functions or as a function
    def add_test(self, new_test):
        if type(new_test) == types.FunctionType:
            self.tests += [new_test]
        elif type(new_test) == list:
            self.tests += new_test

    def __run_all_tests_on_one_row(self, data_row):
        if self.tests:
            results = []
            for t in self.tests:
                results += [t(data_row)]

            return results
        else:
            print("there are no tests to run")

    def anotate_all_sequences(self):
        sql_cursor = self.__create_cursor()

        sequences = list(range(1, self.database_size))

        for oeis_id in self.progressBar(sequences, prefix = self.category_name + ' progress:', suffix = 'Complete', length = 50):
            data_dict = self.__get_data_row_as_dict(sql_cursor,oeis_id)
            results = self.__run_all_tests_on_one_row(data_dict)
            final_result = self.aggregator(results)
            self.anotations[oeis_id] = final_result

    def save_to_overview(self):
        try:
            f = open(self.file_name_overview, "r+t")
            old_header = f.readline().replace("\n","").replace("# ","").replace(" ","")
            old_header_list = old_header.split(",")
            f.close()
            old_data = np.loadtxt(self.file_name_overview, delimiter=',',dtype = int, skiprows = 1)

            if self.category_name in old_header_list:
                new_header = old_header
            else:
                new_header = old_header + "," + self.category_name

        except:
            print("file not found, creating new one")
            new_header = "rating, " + self.category_name
            old_data = np.reshape(np.arange(0, 5), (5, 1))
            old_header_list = []

        overview_of_this_anotator = np.zeros((5,1), dtype = int)

        for i in range(5):
            overview_of_this_anotator[i] = np.count_nonzero(self.anotations == i)


        if self.category_name in old_header_list:
            index = old_header_list.index(self.category_name)
            new_data = old_data
            new_data[:,index] = np.reshape(overview_of_this_anotator, (5,))
        else:
            new_data = np.hstack((old_data, overview_of_this_anotator))
        savetxt(self.file_name_overview, new_data.astype(int), fmt="%u", delimiter = ",", header = new_header)

    def save_anotations_to_file(self):

        try:
            f = open(self.file_name_results, "r+t")
            old_header = f.readline().replace("\n","").replace("# ","").replace(" ","")
            old_header_list = old_header.split(",")
            f.close()
            old_data = np.loadtxt(self.file_name_results, delimiter=',',dtype = int, skiprows = 1)




            if self.category_name in old_header_list:
                index = old_header_list.index(self.category_name)
                new_header = old_header
                new_data = old_data
                new_data[:, index] = self.anotations

            else:
                data = np.reshape(self.anotations, (self.database_size, 1))
                new_header = old_header + "," + self.category_name
                new_data = np.hstack((old_data, data))

        except FileNotFoundError:
            print("file not found, creating new one")
            new_header = "oeis_id, " + self.category_name
            oeis_ids = np.reshape(np.arange(0, self.database_size), (self.database_size, 1))
            data = np.reshape(self.anotations, (self.database_size, 1))
            new_data = np.hstack((oeis_ids, data))

        savetxt(self.file_name_results, new_data.astype(int), fmt="%u", delimiter = ",", header = new_header)



    #progress bar from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    def progressBar(self, iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        total = len(iterable)
        # Progress Bar Printing Function
        def printProgressBar (iteration):
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Initial Call
        printProgressBar(0)
        # Update Progress Bar
        for i, item in enumerate(iterable):
            yield item
            printProgressBar(i + 1)
        # Print New Line on Complete
        print()


#tests need to check wheter needed data_dict elements are None or empty!



#returns 1 if any of the words in "words_to_search" (str or list of str) is found in the database field give by "category" (str).
#if no words are matched, returns 0.
#if the respective field in the database is empty, returns 4.
def basic_word_search(data_dict, words_to_search, category, case_sensitve = False):

    if data_dict[category] is None:
        return 4

    if type(words_to_search) == str:
        words_to_search = [words_to_search]

    for word in words_to_search:
        if case_sensitve == True:
            if word in data_dict[category]:
                return 1
        else:
            if word.lower() in data_dict[category].lower():
                return 1
    return 0
