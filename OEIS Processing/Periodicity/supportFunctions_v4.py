# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:56:35 2021

@author: Emanuel
"""

import numpy as np
from numpy import asarray
from numpy import savetxt



def test_one_sequence_periodic(oeis_id, sql_cursor, verbose = 0):
    sequence = get_sequence(sql_cursor, oeis_id)
    min_periods = 3
    max_period_length = 10000

    if sequence is None:
        if verbose > 1:
            print("sequence is none: ",oeis_id)
        return 4
    
    if check_keywords(sql_cursor, oeis_id):
        return 5
    
    for i in range(1,max_period_length):
        
        if verbose > 1:
            print("period: ",i)
        
        if len(sequence) >= min_periods*i: 
            if test_periodicity(sequence,min_periods,i,verbose,oeis_id) == 1:
                if verbose > 0:
                    print(str(oeis_id) + " is periodic with period " + str(i))
                
                #return [1,i,int(np.floor(len(sequence)/i))]
                return 1
        else:
            return 3
        
    return 0


def test_one_sequence_periodic_v2(oeis_id, sql_cursor, verbose = 0):
    sequence = get_sequence(sql_cursor, oeis_id)
    min_periods = 3
    max_period_length = 100

    if sequence is None:
        if verbose > 1:
            print("sequence is none: ",oeis_id)
        return 4
    
    if check_keywords(sql_cursor, oeis_id):
        return 5
    
    autocor = autocorrelate_test(sequence, verbose, oeis_id)
    
    if test_periodicity(sequence,min_periods,autocor,verbose,oeis_id) == 1:
        for i in range(1,autocor + 1):
            if len(sequence) >= min_periods*i: 
                if test_periodicity(sequence,min_periods,i,verbose,oeis_id) == 1:
                    if verbose > 0:
                        print(str(oeis_id) + " is periodic with period " + str(i))

                    return 1
            else:
                return 3
            
    else:
        for i in range(1,max_period_length):
        
            if verbose > 1:
                print("period: ",i)
            
            if len(sequence) >= min_periods*i: 
                if test_periodicity(sequence,min_periods,i,verbose,oeis_id) == 1:
                    if verbose > 0:
                        print(str(oeis_id) + " is periodic with period " + str(i))
                    return 1
            else:
                return 3
    
    return 0
    
    
def test_periodicity(y, min_periods, period_length, verbose, oeis_id):
    if y[0] != y[period_length]:
        return 0
    
    base = y[:period_length]
    
    if verbose > 1:
        print("repetitions: ", int(np.ceil(len(y)/len(base))))
    
    repeated_base = np.tile(base, int(np.ceil(len(y)/len(base))))[:len(y)]
    assert len(repeated_base) == len(y)
    
    if verbose > 1:
        print("true: ", y)
        print("rep: ", repeated_base)
    
    sae = sum(abs(y - repeated_base)) #summed absolute error
    if sae == 0:
        return 1
    return 0
    
    

def saveArray(isPoly,filename):
    data = asarray(isPoly)
    savetxt(filename, data.astype(int), fmt='%u', delimiter=',')
    print('Saved!')
    
    
def check_keywords(sql_cursor, oeis_id):
    sql_cursor.execute('SELECT keywords FROM oeis_entries WHERE oeis_id = ?',(str(oeis_id),))
    dataRow = sql_cursor.fetchone()[0]
    if "fini" in dataRow or "dead" in dataRow:
        return True
    return False


def autocorrelate_test(y,verbose,oeis_id):
    autocor = np.correlate(y,y,'full')
    autocor = autocor[int(len(autocor)/2):]
    
    if verbose > 1:
        print("autocor: ", autocor)
    
    periodicity = np.argmax(autocor[1:]) + 1
    
    return periodicity

def get_sequence(sql_cursor, oeis_id):
    sql_cursor.execute('SELECT value_list FROM oeis_entries WHERE oeis_id = ?',(str(oeis_id),))
    dataRow = sql_cursor.fetchone()
    
    ##check for empty or non existent sequences 
    if dataRow == None or dataRow[0] == "":
        return None
    
    #parse the number of the sequence - keep in mind the offset of the sequence (i.e. the starting point)
    y = np.asarray(list(map(int, dataRow[0].split(','))),dtype = "object")    #the values of the sequence
    
    return y