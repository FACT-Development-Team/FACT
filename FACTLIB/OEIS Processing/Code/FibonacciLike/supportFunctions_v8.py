# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 09:48:59 2021

@author: Emanuel
"""

import re
import numpy as np
from numpy import asarray
from numpy import savetxt

def check_one_sequence(oeis_id, sql_cursor, verbose = 0):
    columns = ['name', 'formulas']
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)
    
    if dataRow == None:
        return [4,"",4,""]
    
    name_results = check_entry(dataRow[0])
    formulas_results = check_entry(dataRow[1])
    
    return name_results + formulas_results
    
def check_entry(dataRow):
    if dataRow == None or dataRow == "":
        return [4,""]
    
    else: 
        return match_regex(dataRow)


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

#by Ned Batchelder from https://stackoverflow.com/questions/7001144/range-over-character-in-python
def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)

def match_regex(string_to_check):
    #test = "sdfsa *dasd xy a(n) = 2*a(n-1) - 32a(n-2) + a(n +3)."
    #test = "	Pell numbers: a(0) = 0, a(1) = 1; for n > 1, a(n) = 2*a(n-1) + a(n-2)."
    s_low_nospace = string_to_check.lower().replace(" ", "")
    
    
    for c in char_range('a', 'z'):
        R = r"[0-9]*\*?" + c + r"\(n[\+\-][0-9]+\)"
        regex = c + r"\(n\)=" + R + r"[\+\-]" + R + r"([\+\-]" + R + r")*"
        #regex = r".*" + c + r"\(n\)=" + R + r"[\+\-]" + R + r"([\+\-]" + R + r")*"
        #regex = c + r"\(n\)="
        
        
        p = re.compile(regex)
        m = p.search(s_low_nospace)
        
        if m:
            found_string = m.group()
            return [1,found_string]
    
    return [0, ""]













