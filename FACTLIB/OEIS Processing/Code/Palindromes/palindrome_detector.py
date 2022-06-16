# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 14:45:14 2021

@author: Emanuel
"""


import numpy as np
import sqlite3
import time
import keyboard
import supportFunctions_v9 as sf






start_time = time.time()

filename = 'isPalindrome_v1.csv'

connection = sqlite3.connect('C:/OEISDB/oeis_parsed.sqlite3')
sql_cursor = connection.cursor()

sql_cursor.execute('SELECT MAX(oeis_id) FROM oeis_entries')
maxIndex = sql_cursor.fetchone()[0]

verbose = 0


try: 
    isPalindrome = np.loadtxt(filename, delimiter=',')
except OSError:
    isPalindrome = np.zeros([342305,6])
    

    
startingID = (isPalindrome[1:]==0).argmax(axis=0)[0]

for oeis_id in range(startingID,maxIndex + 1):
     
    if oeis_id % 1000 == 0:
        print("id: ",oeis_id)
        end_time = time.time()
        print("Time taken: " + str(end_time - start_time))
        print("Estimated remaining time: ", (end_time - start_time)*((342305-startingID)/(oeis_id+1-startingID) - 1))
        
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('s'):  # if key 'q' is pressed
            sf.saveArray(isPalindrome, filename)
            
            end_time = time.time()
            print("Time taken: " + str(end_time - start_time))
            break  # finishing the loop  
    except:
        break  # if user pressed a key other than the given key the loop will break
    
    
    
    results = sf.check_one_sequence(oeis_id, sql_cursor, verbose)
    
    #0: oeis_id
    #1: entries are palindromes
    #2: name contains palindrome
    #3: comments contain palindrome
    #4: Mathematica contains palindrome
    #5: keywords contain "base"
    isPalindrome[oeis_id,0] = oeis_id
    isPalindrome[oeis_id,1:] = results
    
    
    
sf.saveArray(isPalindrome,filename)

end_time = time.time()
print("Time taken: " + str(end_time - start_time))
    
    
    
    

