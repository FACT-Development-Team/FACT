# -*- coding: utf-8 -*-
"""
Created on Wed May  5 09:34:06 2021

@author: Emanuel
"""





import numpy as np
from numpy import asarray
from numpy import savetxt

    
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