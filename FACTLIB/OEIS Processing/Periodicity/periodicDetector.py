# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:52:59 2021

@author: Emanuel
"""

import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v4 as sf

start_time = time.time()

filename = 'isPeriodic_v2.csv'

connection = sqlite3.connect('C:/OEISDB/oeis_parsed.sqlite3')
sql_cursor = connection.cursor()

sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
maxIndex = sql_cursor.fetchone()[0]



try: 
    isPeriodic = np.loadtxt(filename, delimiter=',')
except OSError:
    isPeriodic = np.zeros([342305,2])
    
startingID = (isPeriodic[1:]==0).argmax(axis=0)[0]


for oeis_id in range(startingID,maxIndex + 1):
    
    if oeis_id % 1000 == 0:
        print("id: ",oeis_id)
        end_time = time.time()
        print("Time taken: " + str(end_time - start_time))
        print("Estimated remaining time: ", (end_time - start_time)*(342305/(oeis_id+1) - 1))
    
    if isPeriodic[oeis_id,1] == 0:
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('s'):  # if key 'q' is pressed
                sf.saveArray(isPeriodic, filename)
                
                end_time = time.time()
                print("Time taken: " + str(end_time - start_time))
                break  # finishing the loop  
        except:
            break  # if user pressed a key other than the given key the loop will break
            
        isPeriodic[oeis_id,0] = oeis_id
        isPeriodic[oeis_id,1] = sf.test_one_sequence_periodic(oeis_id, sql_cursor, 1)
        if isPeriodic[oeis_id,1] == 1:
            print("new sequence added! ", oeis_id)
    
    
    
            
                
sf.saveArray(isPeriodic,filename)

end_time = time.time()
print("Time taken: " + str(end_time - start_time))