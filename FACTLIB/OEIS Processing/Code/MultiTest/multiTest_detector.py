# -*- coding: utf-8 -*-
"""
Created on Tue May 25 10:18:30 2021

@author: Emanuel
"""


import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v16 as sf





def check_one_sequence(oeis_id, sql_cursor, verbose = 0):
    
    #subways: 1
    #trees: 1
    #graph: 10
    #alphabetical: 5
    
    
    functions = [sf.check_subways,
                 sf.check_trees,
                 sf.check_graph,
                 sf.check_alphabetical,
                 sf.check_chess,
                 sf.check_algorithm_steps,
                 sf.check_polyominoes,
                 sf.check_dead,
                 sf.check_lattice_walks,
                 sf.check_coordination_sequence,
                 sf.check_cellular_automaton,
                 sf.check_meander]
    
    
    result = []
    for f in functions:
        result = result + f(oeis_id, sql_cursor)
    
    result = np.reshape(result, (1,len(result)))
    
    return result




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
    filename = 'is_Multitest_v1.csv'
    number_of_columns = 38
    
    start_time = time.time()
    
    sql_cursor = create_cursor()
    sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
    maxIndex = sql_cursor.fetchone()[0]
    
    is_final_result = load_file(filename, number_of_columns)
    startingID = (is_final_result[1:]==0).argmax(axis=0)[0]
        
    
    new_classified_counter = 0
    
    for oeis_id in range(startingID,maxIndex + 1):
         
        if oeis_id % 1000 == 0:
            print("id: ",oeis_id)
            end_time = time.time()
            print("Time taken: " + str(end_time - start_time))
            print("Estimated remaining time: ", (end_time - start_time)*((342305-startingID)/(oeis_id+1-startingID) - 1))
            
            print("total new classified: ", new_classified_counter)
            
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('s'):  # if key 'q' is pressed
                sf.saveArray(is_final_result, filename)
                
                end_time = time.time()
                print("Time taken: " + str(end_time - start_time))
                break  # finishing the loop  
        except:
            break  # if user pressed a key other than the given key the loop will break
        
        
        
        results = check_one_sequence(oeis_id, sql_cursor, verbose)
        
        #0: 
        #1: 
        #2: 
        #3: 
        #4: 
        is_final_result[oeis_id,0] = oeis_id
        is_final_result[oeis_id,1:] = results
        
        if np.count_nonzero(results == 1) > 0:
            new_classified_counter += 1
        
        
    sf.saveArray(is_final_result,filename)
    
    end_time = time.time()
    print("Time taken: " + str(end_time - start_time))