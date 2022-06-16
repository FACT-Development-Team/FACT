# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 09:49:28 2021

@author: Emanuel
"""

import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v3 as sf
from wolframclient.evaluation import WolframLanguageSession













start_time = time.time()



#Creates a connection to the SQL Server
connection = sqlite3.connect('C:/OEISDB/oeis_parsed.sqlite3')
sql_cursor = connection.cursor()

sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
maxIndex = sql_cursor.fetchone()[0]
#print(maxIndex)

session = WolframLanguageSession()

try: 
    isPoly = np.loadtxt('dividedDiffsPolyFullRun7.csv', delimiter=',')
except OSError:
    isPoly = np.zeros([342305,2])
    
startingID = (isPoly[1:]==0).argmax(axis=0)[0]

#isPolyOld = np.loadtxt('dividedDiffsPolyFullRun5.csv', delimiter=',')


for oeis_id in range(startingID,maxIndex + 1):
    
    if oeis_id % 1000 == 0:
        print("id: ",oeis_id)
        end_time = time.time()
        print("Time taken: " + str(end_time - start_time))
    
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('s'):  # if key 'q' is pressed
            sf.saveArray(isPoly)
            
            end_time = time.time()
            print("Time taken: " + str(end_time - start_time))
            break  # finishing the loop
    except:
        break  # if user pressed a key other than the given key the loop will break
        
    isPoly[oeis_id,0] = oeis_id
    isPoly[oeis_id,1] = sf.test_one_sequence(oeis_id, sql_cursor,session)
    
            
                
sf.saveArray(isPoly)

end_time = time.time()
print("Time taken: " + str(end_time - start_time))
        


