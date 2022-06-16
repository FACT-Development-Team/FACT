# -*- coding: utf-8 -*-
"""
Created on Tue May  4 10:15:07 2021

"""
import numpy as np
from numpy import asarray
from numpy import savetxt

def check_one_sequence(oeis_id, sql_cursor, verbose = 0):
    columns = ['name', 'mathematica_programs','keywords']
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)

    if dataRow == None:
        return [4,4,4,4]

    result = check_words([dataRow[2]], ["cofr"]) + check_continued_Fraction([dataRow[0]]) + check_words([dataRow[1]], ["continued fraction", "continuedfraction"])
    return result




def check_continued_Fraction(dataRow):
    words = ["continued fraction"]
    results = []



    for col in dataRow:
        if col == None or col == "":
            results.append(4)
            results.append(4)
        else:
            if "continued fraction convergents" in col.lower():
                results.append(1)
                clean_col = col.lower().replace("continued fraction convergents","")
            else:
                results.append(0)
                clean_col = col.lower()

            results.append(0)
            for word in words:
                if word in clean_col:
                    results[-1] = 1
                    break

    return results

def check_words(dataRow, words):

    results = []

    for col in dataRow:
        if col == None or col == "":
            results.append(4)
        else:
            results.append(0)
            for word in words:
                if word in col.lower():
                    results[-1] = 1
                    break

    assert len(dataRow) == len(results)
    return results

def saveArray(data,filename):
    data = asarray(data)
    savetxt(filename, data.astype(int), fmt='%u', delimiter=',')
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
