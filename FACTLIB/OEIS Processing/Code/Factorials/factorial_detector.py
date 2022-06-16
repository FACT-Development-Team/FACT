# -*- coding: utf-8 -*-
"""
Created on Fri May 28 09:50:48 2021

"""
import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v17 as sf

def check_one_sequence(oeis_id, sql_cursor, verbose = 0):

    functions = [sf.check_binomials,
                 sf.check_factorial,
                 sf.check_double_factorial,
                 sf.check_super_factorial]


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
    filename = 'is_Factorial_v1.csv'
    number_of_columns = 21

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
