# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 15:48:54 2021

"""


import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v7 as sf

start_time = time.time()
verbose = 0


filename = 'decimal_expansion.csv'


connection = sqlite3.connect('C:/OEISDB/oeis_parsed.sqlite3')
sql_cursor = connection.cursor()

sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
maxIndex = sql_cursor.fetchone()[0]



try:
    isDecimalExpansion = np.loadtxt(filename, delimiter=',')
except OSError:
    isDecimalExpansion = np.zeros([342305,5])


startingID = (isDecimalExpansion[1:]==0).argmax(axis=0)[0]


for oeis_id in range(startingID,maxIndex + 1):

    if oeis_id % 1000 == 0:
        end_time = time.time()
        print("id: ", oeis_id)
        print("estimated remaining time: ", (end_time - start_time)*(int(maxIndex)/(oeis_id+1) - 1))

    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('s'):  # if key 'q' is pressed
            sf.saveArray(isDecimalExpansion, filename)

            end_time = time.time()
            print("Time taken: " + str(end_time - start_time))
            break  # finishing the loop
    except:
        break  # if user pressed a key other than the given key the loop will break


    #isDecimalExpansion:
    #column 1: oeis_id
    #column 2: has "decimal expansion" in the name
    #column 3: has keyword "cons"
    #column 4: has keyword "base"
    #column 5: has "decimal expansion" in comments
    isDecimalExpansion[oeis_id,0] = oeis_id
    isDecimalExpansion[oeis_id,1:] = sf.check_one_sequence(oeis_id,sql_cursor, verbose)


sf.saveArray(isDecimalExpansion,filename)

end_time = time.time()
print("Time taken: " + str(end_time - start_time))
