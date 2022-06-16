# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 15:48:54 2021

@author: Emanuel
"""


import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v5 as sf

start_time = time.time()
verbose = 0


filename = 'is_Exponential_v3.csv'
filename_old = 'is_Exponential_v2.csv'

connection = sqlite3.connect('C:/OEISDB/oeis_parsed.sqlite3')
sql_cursor = connection.cursor()

sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
maxIndex = sql_cursor.fetchone()[0]



try: 
    isExponential = np.loadtxt(filename, delimiter=',')
except OSError:
    isExponential = np.zeros([342305,5])
    
try:
    isExponential_old = np.loadtxt(filename_old, delimiter=',')
except OSError:
    print("old file not found")
    
    
startingID = (isExponential[1:]==0).argmax(axis=0)[0]


for oeis_id in range(startingID,maxIndex + 1):
    
    if oeis_id % 1000 == 0:
        end_time = time.time()
        print("id: ", oeis_id)
        print("estimated remaining time: ", (end_time - start_time)*(int(maxIndex)/(oeis_id+1) - 1))

    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('s'):  # if key 'q' is pressed
            sf.saveArray(isExponential, filename)
            
            end_time = time.time()
            print("Time taken: " + str(end_time - start_time))
            break  # finishing the loop  
    except:
        break  # if user pressed a key other than the given key the loop will break
    
    if isExponential_old[oeis_id, 1] in [1,2]:
        isExponential[oeis_id,1] = sf.test_one_sequence_exponential(oeis_id, sql_cursor, verbose)
    
        if isExponential[oeis_id,1] not in [1,2]:
            print(str(oeis_id) + " is no longer marked as exponential")
    
        if verbose > 0:
            print("id: ", oeis_id)
            print("result: ", isExponential[oeis_id,1])
            print(" ")
    else:
        isExponential[oeis_id,1] = isExponential_old[oeis_id,1]
    isExponential[oeis_id,0] = oeis_id
    isExponential[oeis_id,2:] = isExponential_old[oeis_id,2:]
    
    
    
sf.saveArray(isExponential,filename)

end_time = time.time()
print("Time taken: " + str(end_time - start_time))

