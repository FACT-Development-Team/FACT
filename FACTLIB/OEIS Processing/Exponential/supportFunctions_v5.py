# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:56:35 2021

@author: Emanuel
"""

import numpy as np
from numpy import asarray
from numpy import savetxt


def test_one_sequence_exponential(oeis_id, sql_cursor, verbose = 0):
    sequence = get_sequence(sql_cursor, oeis_id)

    if sequence is None:
        if verbose > 1:
            print("sequence is none: ",oeis_id)
        return 4
    
    if len(sequence) < 3:
        return 3 #too few elements
    
    if check_keywords(sql_cursor, oeis_id):
        return 5
    
    try:
        q = calculate_quotients(sequence, verbose)
    except OverflowError:
        return 7
        
    if q is None: 
        return 6
    
    if check_monotonicity(q, verbose):
        response_value = check_quotient_approaching_something(sequence,q, verbose)
        
        return response_value
    
    return 0
    
    
def check_quotient_approaching_something(sequence,q, verbose):
    strip_length = 30
    epsilon = 10e-5
    
    diff_of_q = calculate_differences(q, verbose)
    
    if verbose > 0:
        print("q: ", q)
        print("diff of q: ", diff_of_q)
    
    
    if diff_of_q[-1] == 0 and check_constant(q[-strip_length:], verbose):
        if verbose > 0:
            print("sequence of quotients seems to approach a fixed value")
        return 1
    
    last_elem_sequence = diff_of_q[-1]*np.ones(strip_length,"object")
    
    if len(diff_of_q) < strip_length:
        return 3 #too few elements
    
    if sum(diff_of_q[-strip_length:] - last_elem_sequence) < strip_length*epsilon:
        if verbose > 0:
            print("sequence of quotients seems to slooowly approach a fixed value")
        return 2
    
    
    return False
    
    
def check_monotonicity(sequence, verbose):
    difference = calculate_differences(sequence, verbose)
    
    if np.count_nonzero(difference >= 0) == len(sequence)-1 or np.count_nonzero(difference <= 0) == len(sequence)-1:
        return True
    return False
    
def check_constant(sequence, verbose):
    if np.count_nonzero(sequence == sequence[0]) == len(sequence):
        return True
    return False
    
def calculate_quotients(sequence,verbose):
    shifted_sequence = np.roll(sequence, -1)[:-1]
    cut_sequence = sequence[:-1]
    
    if verbose > 1:
        print("cut:", cut_sequence)
        print("shift:", shifted_sequence)
    
    if np.count_nonzero(shifted_sequence == 0) == 0:
        try:
            quotients = cut_sequence/shifted_sequence
        except OverflowError:
            raise OverflowError
        
        return quotients
    
    else: 
        return None
    


def calculate_differences(sequence, verbose):
    shifted_sequence = np.roll(sequence, -1)[:-1]
    cut_sequence = sequence[:-1]
    
    difference = cut_sequence - shifted_sequence
    
    if verbose > 1:
        print("cut:", cut_sequence)
        print("shift:", shifted_sequence)
        
    return difference
    
    
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

def get_sequence(sql_cursor, oeis_id):
    sql_cursor.execute('SELECT value_list FROM oeis_entries WHERE oeis_id = ?',(str(oeis_id),))
    dataRow = sql_cursor.fetchone()
    
    ##check for empty or non existent sequences 
    if dataRow == None or dataRow[0] == "":
        return None
    
    #parse the number of the sequence - keep in mind the offset of the sequence (i.e. the starting point)
    y = np.asarray(list(map(int, dataRow[0].split(','))),dtype = "object")    #the values of the sequence
    
    return y