# -*- coding: utf-8 -*-
"""
Created on Thu May  6 09:20:07 2021

@author: Emanuel
"""


import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v14 as sf



def check_one_sequence(oeis_id, sql_cursor, verbose = 0):
    columns = ['name', 'mathematica_programs','formulas']
    words = ["root"]
    words_to_ignore = ["rooted"]
    column_names = ', '.join(columns)
    dataRow = sf.get_db_entry(oeis_id, sql_cursor, column_names)
    
    if dataRow == None:
        return [[4,4,4,4,4,4,4],["","","",""]]
    
    regex_name = sf.regex_root_name(dataRow[0])
    regex_formula_in_name = sf.regex_root_formula(dataRow[0])
    regex_formula_in_mathematica = sf.regex_root_formula(dataRow[1])
    regex_formula_in_formulas = sf.regex_root_formula(dataRow[2])
    
    integer_result = sf.check_words(dataRow[:], words, words_to_ignore) + [regex_name[0], regex_formula_in_name[0], regex_formula_in_mathematica[0], regex_formula_in_formulas[0]]
    text_result = [regex_name[1],regex_formula_in_name[1], regex_formula_in_mathematica[1], regex_formula_in_formulas[1]]
    return [integer_result, text_result]






def main():
    start_time = time.time()
    
    filename = 'isRoot_v1.csv'
    filename_strings = "root_strings_v1.csv"
    
    connection = sqlite3.connect('C:/OEISDB/oeis_parsed.sqlite3')
    sql_cursor = connection.cursor()
    
    sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
    maxIndex = sql_cursor.fetchone()[0]
    
    verbose = 0
    
    
    try: 
        isRoot = np.loadtxt(filename, delimiter=',')
    except OSError:
        isRoot = np.zeros([342305,8])
        
    try: 
        root_strings = np.loadtxt(filename_strings, delimiter = ',',dtype = '<U30')
    except OSError:
        root_strings= np.zeros([342305,5], dtype = '<U30')
        
        
    startingID = (isRoot[1:]==0).argmax(axis=0)[0]
    
    for oeis_id in range(startingID,maxIndex + 1):
         
        if oeis_id % 1000 == 0:
            print("id: ",oeis_id)
            end_time = time.time()
            print("Time taken: " + str(end_time - start_time))
            print("Estimated remaining time: ", (end_time - start_time)*((342305-startingID)/(oeis_id+1-startingID) - 1))
            
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('s'):  # if key 'q' is pressed
                sf.saveArray(isRoot, filename)
                
                end_time = time.time()
                print("Time taken: " + str(end_time - start_time))
                break  # finishing the loop  
        except:
            break  # if user pressed a key other than the given key the loop will break
        
        
        
        [results, string_results] = check_one_sequence(oeis_id, sql_cursor, verbose)
        
        #results:
        #0: oeis_id
        #1: name contains root but not rooted
        #2: mathematica contains root but not rooted
        #3: formulas contains root but not rooted
        #4: name contains a string like: "square root" or "fifth-root" ,using the regex: (( )|(^))(([a-z]+)|(\d+th))(( )|(-))root 
        #5: name contains a string like: "^(5/3)" or "^(n/8)", using the regex: ((\^\((n\/\d+)\))|(\^\((\d+\/\d+)\)))
        #6: mathematica contains a string like: "^(5/3)" or "^(n/8)", using the regex: ((\^\((n\/\d+)\))|(\^\((\d+\/\d+)\)))
        #7: formulas contains a string like: "^(5/3)" or "^(n/8)", using the regex: ((\^\((n\/\d+)\))|(\^\((\d+\/\d+)\)))
        
        isRoot[oeis_id,0] = oeis_id
        isRoot[oeis_id,1:] = results
        
        #string_results:
        #0: oeis_id
        #1: contains the first word of the string found in index 4 of results
        #2: contains the power in the string found in index 5 of results
        #3: contains the power in the string found in index 6 of results
        #4: contains the power in the string found in index 7 of results
        
        root_strings[oeis_id,0] = str(oeis_id)
        root_strings[oeis_id,1:] = string_results
        
        
    sf.saveArray(isRoot,filename)
    sf.saveArray_text(root_strings,filename_strings)
    
    end_time = time.time()
    print("Time taken: " + str(end_time - start_time))