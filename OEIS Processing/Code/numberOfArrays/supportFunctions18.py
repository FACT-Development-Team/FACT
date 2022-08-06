# -*- coding: utf-8 -*-
"""
Created on Fri May 28 13:59:32 2021

@author: Emanuel
"""


import re
import numpy as np
from numpy import asarray
from numpy import savetxt


def number_of_arrays_regex(string_to_check):
    p = re.compile(r"number of( (?:n|\d+)x(?:n|\d+))?( \d..\d)? arrays")
    m = p.match(string_to_check.lower())

    if m:
        if m.group(1):
            return [1,1]
        else:
            return [1,0]
    else:
        return [0,0]

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