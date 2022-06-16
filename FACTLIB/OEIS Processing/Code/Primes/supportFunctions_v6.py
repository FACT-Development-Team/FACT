# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 11:10:29 2021

@author: Emanuel
"""

import numpy as np
from numpy import asarray
from numpy import savetxt
from sympy.ntheory import isprime


def check_one_sequence(oeis_id, sql_cursor, verbose = 0):
    results = [oeis_id, test_elements(oeis_id, sql_cursor, verbose)]
    text_results = test_text_blocks(oeis_id, sql_cursor, verbose)
    
    for i in range(max(np.shape(text_results))):
        results.append(text_results[1,i])
        
    return results
    

def test_elements(oeis_id, sql_cursor, verbose = 0):
    column_name = 'value_list'

    
    sequence = get_db_entry(oeis_id, sql_cursor, column_name, verbose)
    
    if sequence is None:
        return 4
    
    for n in sequence:
        if n > 2e64:
            return 8
        
        if not isprime(n):
            return 0
    return 1


def test_text_blocks(oeis_id, sql_cursor, verbose = 0):
    columns = ['name', 'mathematica_programs', 'comments', 'formulas', 'maple_programs', 'other_programs']
    column_names = ', '.join(columns)
    
    results = np.zeros((2,len(columns)), object)
    results[0,:] = columns

    keywords = ['prime']
    
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names, verbose)
    
    if dataRow is None:
        results[1,:] = np.ones((1,len(columns)), object)*4
        return results
    
    for col in range(len(columns)):
        if dataRow[col] is not None and dataRow[col] != '':
            for keyword in keywords:
                if keyword in dataRow[col].lower():
                    results[1,col] = 1
        else:
            results[1,col] = 4 #entry is None or ""
    return results

def test_title(oeis_id, sql_cursor, verbose = 0):
    column_name = 'name'
    keywords = ['prime']
    
    title = get_db_entry(oeis_id, sql_cursor, column_name, verbose)
    
    for keyword in keywords:
        if keyword in title:
            if verbose > 0:
                print("keyword " + keyword + " was found in " + title)
            #occurances = title.count(keyword)
            
            
            
            return 1
    
    return 0 
    
def test_mathematica(oeis_id, sql_cursor, verbose = 0):
    column_name = 'mathematica_programs'
    keywords = ['prime']
    
    mathematica = get_db_entry(oeis_id, sql_cursor, column_name, verbose)
    
    for keyword in keywords:
        if keyword in mathematica:
            if verbose > 0:
                print("keyword " + keyword + " was found in " + mathematica)
            #occurances = title.count(keyword)
            
            
            
            return 1
    
    return 0
    
    
def test_comments(oeis_id, sql_cursor, verbose = 0):
    column_name = 'comments'
    keywords = ['prime']
    
    title = get_db_entry(oeis_id, sql_cursor, column_name, verbose)
    
    for keyword in keywords:
        if keyword in title:
            if verbose > 0:
                print("keyword " + keyword + " was found in " + title)
            #occurances = title.count(keyword)
            
            
            
            return 1
    
    return 0
    
def test_formulas(oeis_id, sql_cursor, verbose = 0):
    column_name = 'formulas'
    keywords = ['prime']
    
    title = get_db_entry(oeis_id, sql_cursor, column_name, verbose)
    
    for keyword in keywords:
        if keyword in title:
            if verbose > 0:
                print("keyword " + keyword + " was found in " + title)
            #occurances = title.count(keyword)
            
            
            
            return 1
    
    return 0

def test_maple(oeis_id, sql_cursor, verbose = 0):
    column_name = 'maple_programs'
    keywords = ['prime']
    
    title = get_db_entry(oeis_id, sql_cursor, column_name, verbose)
    
    for keyword in keywords:
        if keyword in title:
            if verbose > 0:
                print("keyword " + keyword + " was found in " + title)
            #occurances = title.count(keyword)
            
            
            
            return 1
    
    return 0

def test_other_programs(oeis_id, sql_cursor, verbose = 0):
    column_name = 'other_programs'
    keywords = ['prime']
    
    title = get_db_entry(oeis_id, sql_cursor, column_name, verbose)
    
    for keyword in keywords:
        if keyword in title:
            if verbose > 0:
                print("keyword " + keyword + " was found in " + title)
            #occurances = title.count(keyword)
            
            
            
            return 1
    
    return 0
    
    
def get_db_entry(oeis_id, sql_cursor, column_name, verbose = 0):
    sql_cursor.execute('''SELECT {} FROM oeis_entries WHERE oeis_id = ?'''.format(column_name),(str(oeis_id),))
    #sql_cursor.execute('SELECT name FROM oeis_entries WHERE oeis_id = ?',(str(oeis_id),))
    #sql_cursor.execute("select :column_name from oeis_entries where oeis_id =:oeis_id",{"column_name": column_name, "oeis_id": str(oeis_id)})
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


def saveArray(isPoly,filename):
    data = asarray(isPoly)
    savetxt(filename, data.astype(int), fmt='%u', delimiter=',')
    print('Saved!')