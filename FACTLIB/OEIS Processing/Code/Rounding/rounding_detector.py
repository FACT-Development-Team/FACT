# -*- coding: utf-8 -*-
"""
Created on Wed May  5 09:33:52 2021

@author: Emanuel
"""


import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v13 as sf


def check_one_sequence(oeis_id, sql_cursor, verbose = 0):
    columns = ['name', 'mathematica_programs','formulas']
    wordsText = ["rounded","rounding", "ceiling", "floor"]
    wordsFormula = ["round", "ceil", "floor"]
    column_names = ', '.join(columns)
    dataRow = sf.get_db_entry(oeis_id, sql_cursor, column_names)
    
    if dataRow == None:
        return [4,4,4]
    
    result = sf.check_words([dataRow[0]], wordsText) + sf.check_words(dataRow[1:], wordsFormula)
    return result

def main():
    start_time = time.time()
    
    filename = 'isRounded_v1.csv'
    
    connection = sqlite3.connect('C:/OEISDB/oeis_parsed.sqlite3')
    sql_cursor = connection.cursor()
    
    sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
    maxIndex = sql_cursor.fetchone()[0]
    
    verbose = 0
    
    
    try: 
        isRounded_v1 = np.loadtxt(filename, delimiter=',')
    except OSError:
        isRounded_v1 = np.zeros([342305,3])
        
        
    startingID = (isRounded_v1[1:]==0).argmax(axis=0)[0]
    
    for oeis_id in range(startingID,maxIndex + 1):
         
        if oeis_id % 1000 == 0:
            print("id: ",oeis_id)
            end_time = time.time()
            print("Time taken: " + str(end_time - start_time))
            print("Estimated remaining time: ", (end_time - start_time)*((342305-startingID)/(oeis_id+1-startingID) - 1))
            
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('s'):  # if key 'q' is pressed
                sf.saveArray(isRounded_v1, filename)
                
                end_time = time.time()
                print("Time taken: " + str(end_time - start_time))
                break  # finishing the loop  
        except:
            break  # if user pressed a key other than the given key the loop will break
        
        
        
        results = check_one_sequence(oeis_id, sql_cursor, verbose)
        
        #0: oeis_id
        #1: name contains any of ["rounded","rounding", "ceiling", "floor"]
        #2: mathematica contains any of ["round", "ceil", "floor"].
        #3: formulas contains any of ["round", "ceil", "floor"].
        isRounded_v1[oeis_id,0] = oeis_id
        isRounded_v1[oeis_id,1:] = results
        
        
        
    sf.saveArray(isRounded_v1,filename)
    
    end_time = time.time()
    print("Time taken: " + str(end_time - start_time))