# -*- coding: utf-8 -*-
"""
Created on Tue May 25 10:19:37 2021

@author: Emanuel
"""

import re
import numpy as np
from numpy import asarray
from numpy import savetxt


def check_subways(oeis_id, sql_cursor):
    columns = ["name"]
    words = ["subway", "railway"]
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)
    
    if dataRow == None:
        return [4]
    
    return check_words([dataRow], words)

   
def check_trees(oeis_id, sql_cursor):
    columns = ["name"]
    words = ["tree"]
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)
    
    if dataRow == None:
        return [4]
    
    return check_words([dataRow], words)


   
def check_graph(oeis_id, sql_cursor):
    columns = ["name", "comments"]
    words = ["tree", "graph"]
    words_2 = ["node", "edge"]

    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)
    
    if dataRow == None:
        return [4,4,4,4,4,4,4,4,4,4]
    
    result_1 = check_words(dataRow, words)
    result_2 = check_words(dataRow, words_2)
    result_labeled = check_words(dataRow, ["labeled"], ["unlabeled"])
    result_directed = check_words(dataRow, ["directed"], ["undirected"])
    result_triangulation = check_words(dataRow, ["triangulation"])
    
    return result_1 + result_2 + result_labeled + result_directed + result_triangulation
    
    

def check_alphabetical(oeis_id, sql_cursor):
    columns = ["name", "comments", "keywords"]
    #words = ["tree"]
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)
    
    if dataRow == None:
        return [4,4,4,4,4]
    
    result_keyword = check_words([dataRow[2]], ["word"])
    result_alphabetical = check_words(dataRow[:2], ["alphabetical", "alphabet"])
    result_3 = check_words(dataRow[:2], ["letters", "characters"])
    
    
    return result_keyword + result_alphabetical + result_3


def check_chess(oeis_id, sql_cursor):
    columns = ["name", "comments"]
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)
    
    words_1 = ["chess"]
    words_2 = ["king", "rook", "queen", "bishop", "knight", "pawn"]

    if dataRow == None:
       return [4,4,4,4]
    
    result_1 = check_words(dataRow, words_1)
    result_2 = check_words(dataRow, words_2)

    return result_1 + result_2
    
    

def check_algorithm_steps(oeis_id, sql_cursor):
    columns = ["name", "comments"]
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)

    if dataRow == None:
       return [4,4]
    
    result_1 = [regex_algorithm_steps(dataRow[0])]
    result_2 = [regex_algorithm_steps(dataRow[1])]

    return result_1 + result_2
    

def check_polyominoes(oeis_id, sql_cursor):
    columns = ["name", "comments"]
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)
    
    words_1 = ["polyominoes"]

    if dataRow == None:
       return [4,4]
    
    result_1 = check_words(dataRow, words_1)

    return result_1
    
    

def check_dead(oeis_id, sql_cursor):
    columns = ["name", "keywords"]
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)
    
    words_1 = ["erroneous"]
    words_2 = ["dead"]

    if dataRow == None:
       return [4,4]
    
    result_1 = check_words([dataRow[0]], words_1)
    result_2 = check_words([dataRow[1]], words_2)

    return result_1 + result_2
    
    

def check_lattice_walks(oeis_id, sql_cursor):
    columns = ["name", "comments", "keywords"]
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)
    
    words_1 = ["walk"]

    if dataRow == None:
       return [4,4,4]
    
    result_1 = check_words(dataRow, words_1)


    return result_1

def check_coordination_sequence(oeis_id, sql_cursor):
    columns = ["name"]
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)
    
    words_1 = ["coordination sequence"]

    if dataRow == None:
       return [4]
    
    result_1 = check_words([dataRow], words_1)


    return result_1

def check_cellular_automaton(oeis_id, sql_cursor):
    columns = ["name", "comments"]
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)
    
    words_1 = ["cellular automaton"]

    if dataRow == None:
       return [4,4]
    
    result_1 = check_words(dataRow, words_1)


    return result_1

def check_meander(oeis_id, sql_cursor):
    columns = ["name", "comments"]
    column_names = ', '.join(columns)
    dataRow = get_db_entry(oeis_id, sql_cursor, column_names)


    if dataRow == None:
       return [4,4,4,4]
    
    result_1 = check_words(dataRow, ["meander"], ["semi-meander"])
    result_2 = check_words(dataRow, ["semi-meander"])


    return result_1 + result_2


def regex_algorithm_steps(string_to_check):
    
    if string_to_check:
        p = re.compile(r"number of .*(?:operation|comparison|iteration)")
        m = p.search(string_to_check.lower())
        
        if m:
            return 1
        else:
            return 0
    
    return 4



def check_words(dataRow, words, words_to_ignore = []):
    
    results = []
    
    for col in dataRow:
        if col == None or col == "":
            results.append(4)
        else:
            results.append(0)
            string_to_check = col.lower()
            for antiWord in words_to_ignore:
                string_to_check = string_to_check.replace(antiWord, "")
            for word in words:
                if word in string_to_check:
                    results[-1] = 1
                    break
    
    assert len(dataRow) == len(results)
    return results  

def saveArray(data,filename):
    data = asarray(data)
    savetxt(filename, data.astype(int), fmt='%u', delimiter=',')
    print('Saved!')
    
def saveArray_text(data,filename):
    data = asarray(data)
    savetxt(filename, data,fmt = '%s', delimiter=',')
    print('Saved!')
    
def get_db_entry(oeis_id, sql_cursor, column_name, verbose = 0):
    sql_cursor.execute('''SELECT {} FROM oeis_entries WHERE oeis_id = ?'''.format(column_name),(str(oeis_id),))
    dataRow = sql_cursor.fetchone()
    
    #check for empty or non existent sequences 
    if dataRow == None:
        return None
    
    if column_name == 'value_list':
        if dataRow[0] == "":
            return None
        #parse the number of the sequence - keep in mind the offset of the sequence (i.e. the starting point)
        y = np.asarray(list(map(int, dataRow[0].split(','))),dtype = "object")    #the values of the sequence
        
        return y
    
    if ',' in column_name:
        return dataRow
    return dataRow[0]