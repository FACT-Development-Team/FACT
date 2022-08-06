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
        if q[-1] != 1:
            if verbose > 0:
                print("sequence of quotients seems to approach a fixed value")
            return 1
        else:
            return 8
    
    last_elem_sequence = diff_of_q[-1]*np.ones(strip_length,"object")
    
    if len(diff_of_q) < strip_length:
        return 3 #too few elements
    
    if sum(diff_of_q[-strip_length:] - last_elem_sequence) < strip_length*epsilon:
        if abs(q[-1] - 1) > epsilon:
            if verbose > 0:
                print("sequence of quotients seems to slooowly approach a fixed value")
            return 2
        else:
            return 8

    
    return 0
    
    
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


def string_parser_exponential_v2(sql_cursor, oeis_id, verbose = 0):
    #name and formulas are checked for a pattern like: a(n) = *^(*n*).
    columns = ['name', 'formulas']
    column_names = ', '.join(columns)
    res1 = np.zeros(len(columns))

    dataRow = get_db_entry(oeis_id, sql_cursor, column_names, verbose)
    
    if dataRow == None:
        res1 = np.ones(len(columns))*4
    else:
        for col in range(len(columns)):
            if dataRow[col] != None and dataRow[col] != "":
                formula_entries = dataRow[col].replace(" ","").split("\n")
                
                for formula in formula_entries:
                    if "a(n)=" in formula:
                        after_start = formula.split("a(n)=",1)[1]
                        
                        
                        
                        if "." in after_start:
                            start_to_end = after_start.split(".",1)[0]
                        else:
                            start_to_end = after_start
                              
                        if "^" in start_to_end and not start_to_end.replace("n","").lower().islower():
                            
                            
                            
                            [before_exponent, exponent] = start_to_end.split("^",1)
                            
                            contains_n = False
                        
                        
                            if exponent[0] == 'n':
                                contains_n = True
                            elif exponent[0] == '(':
                                open_bracket = 0
                                for char in exponent:
                                    if char == '(':
                                        open_bracket += 1
                                    if char == ')':
                                        open_bracket -= 1
                                    if open_bracket == 0:
                                        break
                                    if char == 'n':
                                        contains_n = True
                                        
                            if contains_n:
                                if verbose > 0:
                                    print(columns[col] + ": " + formula + " contains exponential with n")
                                res1[col] = 1
            else:
                res1[col] = 4
            
            
    #mathematica_programs are checked for a pattern like: Table[*^(*n*)]

    dataRow = get_db_entry(oeis_id, sql_cursor, "mathematica_programs", verbose)
    
    res2 = np.zeros(1)
    
    if dataRow == None or dataRow[0] == None or dataRow[0] == "":
        res2 = np.ones(1)*4
    else:
        programs = dataRow.replace(" ","").split("\n")
        for prog in programs:
            if "(*" in prog:
                before_comment = prog.split("(*",1)[0]
            else:
                before_comment = prog
            if "Table[" in before_comment:
                after_start = before_comment.split("Table[",1)[1]
                
                if "^" in after_start and not after_start.replace("n","").replace("Rage","").lower().islower():
                                [before_exponent, exponent] = after_start.split("^",1)
                                
                                contains_n = False
                            
                            
                                if exponent[0] == 'n':
                                    contains_n = True
                                elif exponent[0] == '(':
                                    open_bracket = 0
                                    for char in exponent:
                                        if char == '(':
                                            open_bracket += 1
                                        if char == ')':
                                            open_bracket -= 1
                                        if open_bracket == 0:
                                            break
                                        if char == 'n':
                                            contains_n = True
                                            
                                if contains_n:
                                    if verbose > 0:
                                        print("mathematica_programs: " + prog + " contains exponential with n")
                                    res2[0] = 1
                                    

    return np.concatenate((res1, res2))
    

def string_parser_exponential(sql_cursor, oeis_id, verbose = 0):
    beginnings = ["a(n) = ", "a(n)="]
    columns = ['name', 'mathematica_programs', 'formulas', 'maple_programs', 'other_programs']
    column_names = ', '.join(columns)
    results = np.zeros(len(columns))
    
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names, verbose)
    
    #sql_cursor.execute('SELECT formulas FROM oeis_entries WHERE oeis_id = ?',(str(oeis_id),))
    #dataRow = sql_cursor.fetchone()
    
    
    if dataRow == None:
        return np.ones(len(columns))*4
    
    
    for col in range(len(columns)):
        if dataRow[col] is not None and dataRow[col] != '':
            formula_entries = dataRow[col].split("\n")

            for formula in formula_entries:
                #look for "a(n) = "
                
                
                start = False
                for beginning in beginnings:
                    if beginning in formula:
                        start = True
                        after_start = formula.split(beginning,1)[1]
                        
                        if "." in after_start:
                            start_to_end = after_start.split(".",1)[0]
                        else:
                            start_to_end = after_start.split("\n",1)[0]
                        
                
                if start == True:      
                    if "^" in start_to_end and not start_to_end.replace("n","").lower().islower(): #this is true when no letters are contained expect n:
                        [before_exponent, exponent] = start_to_end.split("^",1)
                        
                        
                        contains_n = False
                        
                        
                        if exponent[0] == 'n':
                            contains_n = True
                        elif exponent[0] == '(':
                            open_bracket = 0
                            for char in exponent:
                                if char == '(':
                                    open_bracket += 1
                                if char == ')':
                                    open_bracket -= 1
                                if open_bracket == 0:
                                    break
                                if char == 'n':
                                    contains_n = True
                        else:
                            #print("unexpected first character after '^' : ", exponent[0])
                            #print(formula)
                            pass
                        
                            
                        if contains_n:
                            if verbose > 0:
                                print(columns[col] + ": " + formula + " contains exponential with n")
                            results[col] = 1
                    elif start_to_end.replace("n","").lower().islower() and verbose > 1: #this is true when no letters are contained expect n:
                        print("too many letters before exponent in: ", before_exponent)
        else:
            results[col] = 4 #entry is None or ""
            
    return results
    
                
    
    
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
    