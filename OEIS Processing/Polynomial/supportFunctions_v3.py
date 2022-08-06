# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 16:35:13 2021

@author: Emanuel
"""
from scipy.interpolate import lagrange
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt
from numpy import asarray
from numpy import savetxt
from sympy import Symbol
from sympy.polys.polyfuncs import interpolate

from wolframclient.language import wl
from wolframclient.language import wlexpr


def test_one_sequence(oeis_id, sql_cursor, session, verbose = False, full_check = False):
    [sequence, start] = get_sequence(sql_cursor, oeis_id)
    maxDegree = 30
    
    if sequence == None or start == None:
        if verbose == True:
            print("sequence is none or start is none")
        return 4

    if check_keywords(sql_cursor, oeis_id):
        return 5
    """
    if len(sequence) < maxDegree:
        sequence = generate_Elements(sql_cursor, oeis_id, session, sequence, 120, verbose)
    """   
    if len(sequence) < maxDegree:
        return 3
    
    n = divided_differences(oeis_id,sequence, maxDegree)
    
    
    
    if n != -1:
        if verbose == True:
            print("divided diff did hold, check lagrange")
            
        if len(sequence) < 2*n:
            return 3
            
        return sympy_Fit(oeis_id, sequence, start, n, verbose, full_check)
    else:  
        if verbose == True:
            print("divided diff did not hold")
        return 0
        


def generate_Elements(sql_cursor,oeis_id, session, existing_samples, new_elements = 100, verbose = False):
    splitters = [".(End)", ". (End)", "(End)","End","\n",".\n", ". -" ]
    
    sql_cursor.execute('SELECT formulas,offset_a, mathematica_programs FROM oeis_entries WHERE oeis_id = ?',(str(oeis_id),))
    dataRow = sql_cursor.fetchone()
    
    formulas = dataRow[0]
    offset = dataRow[1]
    mathematica_code = dataRow[2]
    
    
    """
    if mathematica_code != None and mathematica_code != "":
        print("lets try mathematica first ", oeis_id)
        print("code: ", mathematica_code)
        feedback = session.evaluate(mathematica_code)
        print(type(mathematica_code))
        print("feedback: ",feedback)
        samples = np.asarray(session.evaluate(mathematica_code),dtype = "object")[offset:]
    """
    if formulas != None and formulas != "":
        if "G.f.:" in formulas:
            split_one = formulas.split("G.f.:",1)[1]
            
            splitter_positions = [split_one.find(i) for i in splitters]
            minimal_splitter_position = min([i for i in splitter_positions if i > -1])
            gf = split_one[:minimal_splitter_position]
            
            if "x" in gf:
                mathematica_string = 'Quiet[CoefficientList[Series[' + gf + ', {x, 0, '+ str(offset + new_elements - 1) +'}], x]]'
            elif "z" in gf:
                mathematica_string = 'Quiet[CoefficientList[Series[' + gf + ', {z, 0, '+ str(offset + new_elements - 1) +'}], z]]'
            else:
                return existing_samples
            try:
                samples = np.asarray(session.evaluate(mathematica_string),dtype = "object")[offset:]
            except IndexError:
                #print("Index Error ", oeis_id)
                return existing_samples         
        else:
            #print("no GF! ", oeis_id)
            return existing_samples
        
        
        
    else:
        #print("no formulas ", oeis_id)
        return existing_samples
    
    
    if verbose == True:
        print("existing: ",existing_samples)
        print(samples)

    for i in range(len(existing_samples)):
        try:
            assert existing_samples[i] == samples[i]
        except (AssertionError, ValueError,IndexError) :
            #print("assertion failed ", oeis_id)
            return existing_samples

    print("successfully generated new elements: ",oeis_id)
    session.terminate() 
    return samples
    
def saveArray(isPoly):
    data = asarray(isPoly)
    savetxt('dividedDiffsPolyFullRun7.csv', data.astype(int), fmt='%u', delimiter=',')
    print('Saved!')

def create_plot(x,y,start,n,f):
    x_new = np.arange(start-1, len(y)+1, 1)
    plt.yscale("log")
    plt.plot(x, y, 'ro',x_new[:n], f(x_new[:n]), 'b', x_new[n:], f(x_new[n:]), 'g')
    plt.title('Lagrange Polynomial')
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

def remove_last_element(arr):
    return arr[np.arange(arr.size - 1)]

def all_zero(arr):
    for elem in arr:
        if elem:
            return False
    return True

def check_keywords(sql_cursor, oeis_id):
    sql_cursor.execute('SELECT keywords FROM oeis_entries WHERE oeis_id = ?',(str(oeis_id),))
    dataRow = sql_cursor.fetchone()[0]
    if "fini" in dataRow or "dead" in dataRow:
        return True
    return False

def get_sequence(sql_cursor, oeis_id):
    sql_cursor.execute('SELECT value_list, offset_a FROM oeis_entries WHERE oeis_id = ?',(str(oeis_id),))
    dataRow = sql_cursor.fetchone()
    
    ##check for empty or non existent sequences 
    if dataRow == None or dataRow[0] == "":
        return [None,None]
    
    #parse the number of the sequence - keep in mind the offset of the sequence (i.e. the starting point)
    y = list(map(int, dataRow[0].split(',')))    #the values of the sequence
    start = dataRow[1]  #start = the first index of the sequence (probably most often 0 or 1)
    
    return [y,start]

def divided_differences(oeis_id, y, maxDegree = 30):
    
    
    #perform newtons divided difference method
    a = y
    b = np.roll(a,-1)
    i = 0
    while i < min(maxDegree, len(y)):
        a = remove_last_element(b-a) 
        if all_zero(a):
            #we conclude that this sequence could be polynomial and would have degree i
            return i
        
        b = np.roll(a,-1)
        i += 1
        
    # we conclude that this sequence can not be a polynomial of degree smaller than the number of given elements
    return -1


def sympy_Fit(oeis_id, y, start, n, verbose = False, full_check = False):
    assert n != -1
    n += 1
    x = Symbol('x')

    if full_check == True:
        k = len(y)
    else:
        k = min(4*n,len(y))
        
    if verbose == True:
        print("n: ",n)
        print("k: ",k)
        print("len(y): ",len(y))

    assert k > n
    
    datapoints = [ (i+start , y[i] ) for i in range(0, n)]
    
    if verbose == True:
        print("data: ", datapoints)
    
    poly = interpolate(datapoints, x)
    
    y_true = np.asarray(y[n:k],dtype = "object")
    y_pred = np.asarray([poly.subs(x,i) for i in range(start + n, start + n + len(y_true))],dtype = "object")
    assert len(y_true) == len(y_pred)
    
    
    sae = sum(abs(y_true - y_pred))
    if verbose == True:
        print("poly: ", poly)
        #print("true: ",y_true)
        #print("pred: ",y_pred)
        print("sae: ",sae)
    if sae == 0:
        return 1
    return 0
    

def lagrange_Fit(oeis_id, y, start, n = -1, verbose = False):
    plot = False
    full_check = False
    round_extrapolated_values = True
    mae_threshold = 0.5
    mape_threshold = 0
    
    if n == -1:
        maxDegree = 30
        n = 1
    else: 
        n += 1
        maxDegree = n + 1
        
    if full_check == True:
        k = len(y)
    else:
        k = min(2*maxDegree,len(y))
        
    assert k <= len(y) 
    x = np.arange(start,start + len(y))
    
    if verbose == True:
        print("n: ",n)
        print("maxDegree: ",maxDegree)
        
    while n < maxDegree:
        
        try:
            assert n < len(y) #check wheter there are more than n elements in the sequence to prevent an error
        except AssertionError:
            if verbose == True:
                print("sequence is shorter than n")
            return False
        
        #fit a polynomial to the data
        try: 
            f = lagrange(x[:n],y[:n])
            if verbose == True:
                print(f)
        except OverflowError:
            print("overflow on lagrange ", oeis_id)
            return False
    
        
        #extrapolate
        if round_extrapolated_values == True:
            y_pred = np.rint(f(x[n:k])).astype(object)
        else: 
            y_pred = (f(x[n:k])).astype(object)
    
        y_true = np.array(y[n:k],object)
        
        assert len(y_pred) == len(y_true)
        
        #calculate the error of the lagrange polynomial to the real data with different methods
        
        if verbose == True:
                print("y_pred ", y_pred)
                print("y_true ", y_true)
                #print("x ", x)
        if plot == True:
            create_plot(x,y,start,n,f)
        
        try:
            mae = mean_absolute_error(y_true, y_pred)
            if verbose == True:
                print("mae: ", mae)
            if mae == 0 or abs(mae) < mae_threshold:
                if verbose == True and mae != 0:
                    print("made it because of MAE threshold")
                return True
            
        except OverflowError:
            print("OverflowError in oeis_id", oeis_id)
        
        try:
            mape = mean_absolute_percentage_error(y_true,y_pred)
            if verbose == True:
                print("mape", mape)
            if abs(mape) < mape_threshold:
                if verbose == True:
                    print("made it because of MAPE threshold")
                return True
            
        except OverflowError:
            print("OverflowError in oeis_id", oeis_id)
            return False
        
        
        
        
        
            
        n += 1
    
    return False
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    