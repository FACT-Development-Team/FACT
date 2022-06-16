# -*- coding: utf-8 -*-
"""
Created on Mon May 10 10:30:17 2021

@author: Emanuel
"""


import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v15 as sf


def check_one_sequence(oeis_id, sql_cursor, verbose = 0):
    columns = ['name','formulas']
    column_names = ', '.join(columns)
    dataRow = sf.get_db_entry(oeis_id, sql_cursor, column_names)
    
    if dataRow == None:
        return [4,4]
    
    name_seq_sum = sf.regex_simple_sum(dataRow[0])
    formula_seq_sum = sf.regex_simple_sum(dataRow[1])
    name_seq_and_constant = sf.regex_sequence_and_constant(dataRow[0])
    formula_seq_and_constant = sf.regex_sequence_and_constant(dataRow[1]) 
    
    
    result = [name_seq_sum[0], formula_seq_sum[0], name_seq_and_constant[0], formula_seq_and_constant[0]]
    string_result = [name_seq_sum[1], formula_seq_sum[1], name_seq_and_constant[1], formula_seq_and_constant[1]]
    
    if verbose > 0:
        if name_seq_sum[0] == 1:
            print("id: " + str(oeis_id) + ", string: " + name_seq_sum[1])
        if formula_seq_sum[0] == 1:
            print("id: " + str(oeis_id) + ", string: " + formula_seq_sum[1])
        if name_seq_and_constant[0] == 1:
            print("id: " + str(oeis_id) + ", string: " + name_seq_and_constant[1])
        if formula_seq_and_constant[0] == 1:
            print("id: " + str(oeis_id) + ", string: " + formula_seq_and_constant[1])
        
    #result = sf.check_words([dataRow[0]], wordsText) + sf.check_words(dataRow[1:], wordsFormula)
    return [result, string_result]

def create_cursor():
    connection = sqlite3.connect('C:/OEISDB/oeis_parsed.sqlite3')
    sql_cursor = connection.cursor()
    return sql_cursor

def load_file(filename, number_of_columns):
    try: 
        is_final_result = np.loadtxt(filename, delimiter=',')
    except OSError:
        is_final_result = np.zeros([342305,number_of_columns])
        
    return is_final_result
    

def main():
    verbose = 0
    filename = 'is_simple_sum_v2.csv'
    number_of_columns = 5
    
    start_time = time.time()
    
    sql_cursor = create_cursor()
    sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
    maxIndex = sql_cursor.fetchone()[0]
    
    is_final_result = load_file(filename, number_of_columns)
    startingID = (is_final_result[1:]==0).argmax(axis=0)[0]
        
    for oeis_id in range(startingID,maxIndex + 1):
         
        if oeis_id % 1000 == 0:
            print("id: ",oeis_id)
            end_time = time.time()
            print("Time taken: " + str(end_time - start_time))
            print("Estimated remaining time: ", (end_time - start_time)*((342305-startingID)/(oeis_id+1-startingID) - 1))
            
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('s'):  # if key 'q' is pressed
                sf.saveArray(is_final_result, filename)
                
                end_time = time.time()
                print("Time taken: " + str(end_time - start_time))
                break  # finishing the loop  
        except:
            break  # if user pressed a key other than the given key the loop will break
        
        
        
        results = check_one_sequence(oeis_id, sql_cursor, verbose)
        
        #0: oeis_id
        #1: name contains string like "a(n)=15*A052856(n+5)-423*A052856(n-21)+11*A123456(n)"
        #2: formula contains string like "a(n)=15*A052856(n+5)-423*A052856(n-21)+11*A123456(n)"
        #3: name contains string like "A123456(n+1)-12" or "a(n)=A123456(n)/2"
        #4: formula contains string like "A123456(n+1)-12" or "a(n)=A123456(n)/2"
        is_final_result[oeis_id,0] = oeis_id
        is_final_result[oeis_id,1:] = results[0]
        
        
        
        
    sf.saveArray(is_final_result,filename)
    
    end_time = time.time()
    print("Time taken: " + str(end_time - start_time))