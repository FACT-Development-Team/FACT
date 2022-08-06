# -*- coding: utf-8 -*-
"""
Created on Fri May 28 09:51:07 2021

"""


import numpy as np
from numpy import asarray
from numpy import savetxt



def check_binomials(oeis_id, sql_cursor):
    columns = ["name", "formulas", "mathematica_programs"]
    words = ["binomial(", "binomial["]
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)

    if dataRow == None:
        return [4,4,4] #3

    return check_words(dataRow, words)

def check_factorial(oeis_id, sql_cursor):
    columns = ["name", "formulas", "mathematica_programs"]
    words1 = ["factorial"]
    words2 = ["!"]

    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)

    if dataRow == None:
        return [4,4,4,4,4,4] #6

    result1 =  check_words(dataRow, words1)
    result2 =  check_words(dataRow, words2)

    return result1 + result2

def check_double_factorial(oeis_id, sql_cursor):
    columns = ["name", "formulas", "comments", "mathematica_programs"]
    words1 = ["double factorial", "double-factorial", "doublefactorial"]
    words2 = ["!!"]
    words3 = ["multifactorial"]

    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)

    if dataRow == None:
        return [4,4,4,4,4,4,4,4,4] #9

    result1 =  check_words(dataRow, words1)
    result2 =  check_words(dataRow, words2)
    result3 = check_words([dataRow[3]], words3)

    return result1 + result2 + result3

def check_super_factorial(oeis_id, sql_cursor):
    columns = ["name", "comments"]
    words1 = ["super factorial", "super-factorial", "superfactorial"]

    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)

    if dataRow == None:
        return [4,4] #2

    result1 =  check_words(dataRow, words1)

    return result1

def check_words(dataRow, words, words_to_ignore = []):

    results = []

    for col in dataRow:
        if col == None or col == "":
            results.append(4)
        else:
            results.append(0)
            string_to_check = col.lower()
            for antiWord in words_to_ignore:
                string_to_check = string_to_check.replace(antiWord, "")
            for word in words:
                if word in string_to_check:
                    results[-1] = 1
                    break

    assert len(dataRow) == len(results)
    return results

def saveArray(data,filename):
    data = asarray(data)
    savetxt(filename, data.astype(int), fmt='%u', delimiter=',')
    print('Saved!')

def saveArray_text(data,filename):
    data = asarray(data)
    savetxt(filename, data,fmt = '%s', delimiter=',')
    print('Saved!')

def get_db_entry(oeis_id, sql_cursor, column_name, verbose = 0):
    sql_cursor.execute('''SELECT {} FROM oeis_entries WHERE oeis_id = ?'''.format(column_name),(str(oeis_id),))
    dataRow = sql_cursor.fetchone()

    #check for empty or non existent sequences
    if dataRow == None:
        return None

    if column_name == 'value_list':
        if dataRow[0] == "":
            return None
        #parse the number of the sequence - keep in mind the offset of the sequence (i.e. the starting point)
        y = np.asarray(list(map(int, dataRow[0].split(','))),dtype = "object")    #the values of the sequence

        return y

    if ',' in column_name:
        return dataRow
    return dataRow[0]
