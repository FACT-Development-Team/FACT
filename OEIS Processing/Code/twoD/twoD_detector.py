# -*- coding: utf-8 -*-
"""
Created on Tue May  4 16:04:39 2021

@author: Emanuel
"""


import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v12 as sf






start_time = time.time()

filename = 'istwoD_v1.csv'

connection = sqlite3.connect('C:/OEISDB/oeis_parsed.sqlite3')
sql_cursor = connection.cursor()

sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
maxIndex = sql_cursor.fetchone()[0]

verbose = 0


try: 
    istwoD = np.loadtxt(filename, delimiter=',')
except OSError:
    istwoD = np.zeros([342305,5])
    
    
startingID = (istwoD[1:]==0).argmax(axis=0)[0]

for oeis_id in range(startingID,maxIndex + 1):
     
    if oeis_id % 1000 == 0:
        print("id: ",oeis_id)
        end_time = time.time()
        print("Time taken: " + str(end_time - start_time))
        print("Estimated remaining time: ", (end_time - start_time)*((342305-startingID)/(oeis_id+1-startingID) - 1))
        
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('s'):  # if key 'q' is pressed
            sf.saveArray(istwoD, filename)
            
            end_time = time.time()
            print("Time taken: " + str(end_time - start_time))
            break  # finishing the loop  
    except:
        break  # if user pressed a key other than the given key the loop will break
    
    
    
    results = sf.check_one_sequence(oeis_id, sql_cursor, verbose)
    
    #0: oeis_id
    #1: sequence contains keyword "tabl"
    #2: name contains triangular array, square array or rectangular array.
    #3: comments contains triangular array, square array or rectangular array.
    #4: formula contains triangular array, square array or rectangular array.
    istwoD[oeis_id,0] = oeis_id
    istwoD[oeis_id,1:] = results
    
    
    
sf.saveArray(istwoD,filename)

end_time = time.time()
print("Time taken: " + str(end_time - start_time))