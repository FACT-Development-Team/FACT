# -*- coding: utf-8 -*-
"""
Created on Thu May  6 09:20:25 2021

@author: Emanuel
"""


import re
import numpy as np
from numpy import asarray
from numpy import savetxt



def regex_sequence_and_constant(stringToMatch):
    #this regex matches strings like:
        #a(n)=A123456(n)+1
        #a(n)=A123456(n+1)-12
        #a(n)=A123456(n)/2
    if stringToMatch == None or stringToMatch == "":
        return [4,""]
    
    stringToMatch = stringToMatch.replace(" ","")
    
    p = re.compile(r"a\(n\)=(?:\d+\*)*A\d{6}\(n(?:[\+\-]\d+)?\)[\+\-\/\*]\d+")
    m = p.search(stringToMatch)
    
    if m:
        return [1,m.group()]
    else:
        return [0,""]

def regex_simple_sum(stringToMatch):
    #this regex matches strings like:
        #a(n)=A052856(n)+A052856(n)
        #a(n)=A052856(n+5)+A052856(n-21)
        #a(n)=15*A052856(n+5)-423*A052856(n-21)+11*A123456(n)
    
    if stringToMatch == None or stringToMatch == "":
        return [4,""]
    
    stringToMatch = stringToMatch.replace(" ","")
    
    p = re.compile(r"a\(n\)=(?:\d+\*)*A\d{6}\(n(?:[\+\-]\d+)?\)([\+\-](?:\d+\*)*A\d{6}\(n(?:[\+\-]\d+)?\))+")
    m = p.search(stringToMatch)
    
    if m:
        return [1,m.group()]
    else:
        return [0,""]

def regex_root_name(stringToMatch):
    
    if stringToMatch == None or stringToMatch == "":
        return [4,""]
    
    p = re.compile(r"(( )|(^))(([a-z]+)|(\d+th))(( )|(-))root")
    m = p.search(stringToMatch)
    
    if m:
        return [1,m.group(4)] #group 4 contains the order of the rooth for example "fifth" from the string "lorem ipsum fifth root lorem ipsum"
    else:
        return [0,""]
    
def regex_root_formula(stringToMatch):
    
    if stringToMatch == None or stringToMatch == "":
        return [4,""]
    
    p = re.compile(r"((\^\((n\/\d+)\))|(\^\((\d+\/\d+)\)))")
    m = p.search(stringToMatch)
    
    if m:
        if m.group(3):
            return [1,m.group(3)]
        if m.group(5):
            return [1,m.group(5)]
        print("this text should never be printed")
    return [0,""]

    
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