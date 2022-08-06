# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 13:52:29 2021

"""

import numpy as np
from numpy import asarray
from numpy import savetxt






def check_one_sequence(oeis_id, sql_cursor, verbose = 0):
    columns = ['name', 'keywords', 'comments']
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)

    if dataRow == None:
        return [4,4,4,4]

    results = [check_tile(dataRow[0]),
               check_keyword_base(dataRow[1], "cons"),
               check_keyword_base(dataRow[1], "base"),
               check_comments(dataRow[2])]


    return results


def check_keyword_base(keywords, key):
    if keywords == None or keywords == "":
        return 4

    if key in keywords.lower():
        return 1
    return 0

def check_comments(comments):
    words = ["decimal expansion"]

    if comments == None or comments == "":
        return 4

    for word in words:
        if word in comments.lower():
            return 1
    return 0

def check_tile(title):
    words = ["decimal expansion"]

    if title == None or title == "":
        return 4

    for word in words:
        if word in title.lower():
            return 1

    return 0


def saveArray(isPoly,filename):
    data = asarray(isPoly)
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
