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

filename = 'isPoly_v1.csv'
filename_old = 'dividedDiffsPolyFullRun7.csv'

#Creates a connection to the SQL Server
connection = sqlite3.connect('C:/OEISDB/oeis_parsed.sqlite3')
sql_cursor = connection.cursor()

sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
maxIndex = sql_cursor.fetchone()[0]
#print(maxIndex)

session = WolframLanguageSession()

try: 
    isPoly = np.loadtxt(filename, delimiter=',')
except OSError:
    isPoly = np.zeros([342305,6])
    
try: 
    isPoly_old = np.loadtxt(filename_old, delimiter=',')
except OSError:
    print("old file not found")
    
verbose = 0
startingID = (isPoly[1:]==0).argmax(axis=0)[0]

#isPolyOld = np.loadtxt('dividedDiffsPolyFullRun5.csv', delimiter=',')


startingID = (isPoly[1:]==0).argmax(axis=0)[0]

for oeis_id in range(startingID,maxIndex + 1):
     
    if oeis_id % 1000 == 0:
        print("id: ",oeis_id)
        end_time = time.time()
        print("Time taken: " + str(end_time - start_time))
        print("Estimated remaining time: ", (end_time - start_time)*((342305-startingID)/(oeis_id+1-startingID) - 1))
        
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('s'):  # if key 'q' is pressed
            sf.saveArray(isPoly, filename)
            
            end_time = time.time()
            print("Time taken: " + str(end_time - start_time))
            break  # finishing the loop  
    except:
        break  # if user pressed a key other than the given key the loop will break
    
    
    
    results = sf.check_one_sequence(oeis_id, sql_cursor, verbose)
    
    #0: oeis_id
    #1: could fit a polynomial of degree k
    #2: k
    #3: regex found a polynomial in title - 0 or 1                              my regex: r"a\(n\)=((\((\d*(\**n(\^\d*)?)?(([\+\-]\d*(\**n(\^\d*)?)?)*))\))?\*?((\d*(\**n(\^\d*)?)?(([\+\-]\d*(\**n(\^\d*)?)?)*)))?(\d*\/\d)?(\((\d*\/\d)\))?)+"gm
    #4: regex found a polynomial in formula - 0 or 1
    #5: regex found a polynomial in mathematica_programs

    isPoly[oeis_id,0] = oeis_id
    isPoly[oeis_id,1:] = results[0]
    
    
    
sf.saveArray(isPoly,filename)

end_time = time.time()
print("Time taken: " + str(end_time - start_time))


