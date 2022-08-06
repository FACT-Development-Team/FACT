# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 09:48:25 2021

"""


import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v8 as sf






start_time = time.time()

filename = 'isFibonacci_v1.csv'
filename_formula = 'fibonacci_formula_v1.csv'

connection = sqlite3.connect('C:/OEISDB/oeis_parsed.sqlite3')
sql_cursor = connection.cursor()

sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
maxIndex = sql_cursor.fetchone()[0]

verbose = 0


try:
    isFibonacci = np.loadtxt(filename, delimiter=',')
    fibonacciFormula = np.loadtxt(filename_formula, delimiter = ',',dtype = '<U900')
except OSError:
    isFibonacci = np.zeros([342305,3])
    fibonacciFormula = np.zeros([342305,3], dtype = '<U900')



startingID = (isFibonacci[1:]==0).argmax(axis=0)[0]


for oeis_id in range(startingID,maxIndex + 1):

    if oeis_id % 1000 == 0:
        print("id: ",oeis_id)
        end_time = time.time()
        print("Time taken: " + str(end_time - start_time))
        print("Estimated remaining time: ", (end_time - start_time)*((342305-startingID)/(oeis_id+1-startingID) - 1))

    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('s'):  # if key 'q' is pressed
            sf.saveArray(isFibonacci, filename)
            sf.saveArray_text(fibonacciFormula, filename_formula)

            end_time = time.time()
            print("Time taken: " + str(end_time - start_time))
            break  # finishing the loop
    except:
        break  # if user pressed a key other than the given key the loop will break



    isFibonacci[oeis_id,0] = oeis_id

    results = sf.check_one_sequence(oeis_id, sql_cursor, verbose)

    isFibonacci[oeis_id,1] = results[0]
    isFibonacci[oeis_id,2] = results[2]

    fibonacciFormula[oeis_id,0] = str(oeis_id)
    fibonacciFormula[oeis_id,1] = results[1]
    fibonacciFormula[oeis_id,2] = results[3]


sf.saveArray(isFibonacci,filename)
sf.saveArray_text(fibonacciFormula, filename_formula)

end_time = time.time()
print("Time taken: " + str(end_time - start_time))
