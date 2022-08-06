# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 11:08:38 2021

@author: Emanuel
"""


import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v6 as sf




start_time = time.time()

filename = 'isPrime_v1.csv'

connection = sqlite3.connect('C:/OEISDB/oeis_parsed.sqlite3')
sql_cursor = connection.cursor()

sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
maxIndex = sql_cursor.fetchone()[0]

verbose = 0


try: 
    isPrime = np.loadtxt(filename, delimiter=',')
except OSError:
    isPrime = np.zeros([342305,8])
    
startingID = (isPrime[1:]==0).argmax(axis=0)[0]


for oeis_id in range(startingID,maxIndex + 1):
     
    if oeis_id % 1000 == 0:
        print("id: ",oeis_id)
        end_time = time.time()
        print("Time taken: " + str(end_time - start_time))
        print("Estimated remaining time: ", (end_time - start_time)*((342305-startingID)/(oeis_id+1-startingID) - 1))
        
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('s'):  # if key 'q' is pressed
            sf.saveArray(isPrime, filename)
            
            end_time = time.time()
            print("Time taken: " + str(end_time - start_time))
            break  # finishing the loop  
    except:
        break  # if user pressed a key other than the given key the loop will break
    
        
    
    isPrime[oeis_id,0:] = sf.check_one_sequence(oeis_id, sql_cursor, verbose)
        
        
        
sf.saveArray(isPrime,filename)

end_time = time.time()
print("Time taken: " + str(end_time - start_time))