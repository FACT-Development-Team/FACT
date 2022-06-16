# -*- coding: utf-8 -*-
"""
Created on Mon May  3 09:08:47 2021

"""
import numpy as np
from numpy import asarray
from numpy import savetxt

def saveArray(data, filename, my_header = ""):
    data = asarray(data)
    savetxt(filename, data.astype(int), fmt='%u', delimiter=',', header = my_header)
    print('Saved!')

def loadArray(filename, skip = 0):
    try:
        data = np.loadtxt(filename, delimiter=',',dtype = int, skiprows = skip)
    except OSError:
        print("could not load file: ", filename)

    return data

def polyDecision(val):
    if val == 0:
        result = 0
    elif val == 1:
        result = 4
    elif val == 3:
        result = 1
    elif val == 4:
        result = 0
    elif val == 5:
        result = 0

    return result

def poly():
    filename_old = 'dividedDiffsPolyFullRun7.csv'
    isPoly = loadArray(filename_old)
    single_col = np.zeros([342305,1])

    for oeis_id in range(max(np.shape(isPoly))):
        assert isPoly[oeis_id, 0] == oeis_id

        single_col[oeis_id] = polyDecision(isPoly[oeis_id,1])

    return single_col
    #saveArray(single_col, "singleColPoly.csv")


def periodDecision(columns):
    p = columns[0] #perioducity
    #length = columns[1]
    reps = columns[2]

    if p == 0:
        result = 0
    if p == 1:
        if reps >= 30:
            result = 4
        else:
            result = 3
    if p == 3:
        result = 1
    if p == 4:
        result = 0
    if p == 5:
        result = 0

    return result

def period():
    filename_old = 'periodic_infos.csv'
    isData = loadArray(filename_old)
    single_col = np.zeros([342305,1])

    for oeis_id in range(max(np.shape(isData))):
        assert isData[oeis_id, 0] == oeis_id

        single_col[oeis_id] = periodDecision(isData[oeis_id,1:])

    return single_col

def expDecision(columns):
    expo = columns[0]
    name = columns[1]
    formula = columns[2]
    mathematica = columns[3]

    if expo == 0:
        result = 0
    elif expo == 1:
        result = 3
    elif expo == 2:
        result = 2
    elif expo == 3:
        result = 2
    elif expo == 4:
        result = 0
    elif expo == 5:
        result = 0
    elif expo == 6:
        result = 1
    elif expo == 7:
        result = 1
    elif expo == 8:
        result = 0

    if name == 1:
        result += 2
    if formula == 1:
        result += 1
    if mathematica == 1:
        result += 1

    if result >4:
        result = 4

    return result

def exponential():
    filename_old = 'is_Exponential_v3.csv'
    isData = loadArray(filename_old)
    single_col = np.zeros([342305,1])

    for oeis_id in range(max(np.shape(isData))):
        assert isData[oeis_id, 0] == oeis_id

        single_col[oeis_id] = expDecision(isData[oeis_id,1:])

    return single_col

def decimalDecision(columns):
    name = columns[0]
    const = columns[1]
    base = columns[2]
    comments = columns[3]

    result = 0

    if name == 1:
        result += 4
    if comments == 1:
        result += 2
    if const == 1:
        result += 1
    if base == 1:
        result += 1

    if result >4:
        result = 4

    return result

def decimalExpansion():
    filename_old = 'decimal_expansion.csv'
    isData = loadArray(filename_old)
    single_col = np.zeros([342305,1])

    for oeis_id in range(max(np.shape(isData))):
        assert isData[oeis_id, 0] == oeis_id

        single_col[oeis_id] = decimalDecision(isData[oeis_id,1:])

    return single_col


def expansionDecision(columns):
    name = columns[0]
    name_base = columns[1]
    #   base_found = columns[2]
    mathematica = columns[3]
    base = columns[4]
    cons = columns[5]

    result = 0

    if name == 1:
        result += 3
        if name_base == 1:
            result += 1
    if base == 1:
        result += 1
    if cons == 1:
        result += 1
    if mathematica == 1:
        result += 2

    if result >4:
        result = 4

    return result

def expansion():
    filename_old = 'isExpansion_v1.csv'
    isData = loadArray(filename_old)
    single_col = np.zeros([342305,1])

    for oeis_id in range(max(np.shape(isData))):
        assert isData[oeis_id, 0] == oeis_id

        single_col[oeis_id] = expansionDecision(isData[oeis_id,1:])

    return single_col

def fibonacciDecision(columns):
    name = columns[0]
    formula = columns[1]


    result = 0

    if name == 1:
        result += 4
    if formula == 1:
        result += 3

    if result >4:
        result = 4

    return result

def fibonacci():
    filename_old = 'isFibonacci_v1.csv'
    isData = loadArray(filename_old)
    single_col = np.zeros([342305,1])

    for oeis_id in range(max(np.shape(isData))):
        assert isData[oeis_id, 0] == oeis_id

        single_col[oeis_id] = fibonacciDecision(isData[oeis_id,1:])

    return single_col


def palindromeDecision(columns):
    elements = columns[0]
    name = columns[1]
    comments = columns[2]
    mathematica = columns[3]
    base = columns[4]


    result = np.zeros([1,2])
    if elements == 1:
        result[0,0] = 4
    if name == 1:
        result[0,1] += 4
    if comments == 1:
        result[0,1] += 2
        if base == 1:
            result[0,1] += 1
    if mathematica == 1:
        result[0,1] += 2
        if base == 1:
            result[0,1] += 1


    if result[0,1] >4:
        result[0,1] = 4

    return result

def palindrome():
    filename_old = 'isPalindrome_v1.csv'
    isData = loadArray(filename_old)
    single_col = np.zeros([342305,2])

    for oeis_id in range(max(np.shape(isData))):
        assert isData[oeis_id, 0] == oeis_id

        single_col[oeis_id,:] = palindromeDecision(isData[oeis_id,1:])

    return single_col

def primeDecision(columns):
    elements = columns[0]
    name = columns[1]
    mathematica = columns[2]
    comments = columns[3]
    formulas = columns[4]
    maple = columns[5]
    other = columns[6]


    result = np.zeros([1,2])

    if elements == 1:
        result[0,0] = 4
    if elements == 8:
        result[0,0] = 2



    r2 = 0
    if name == 1:
        r2 += 4
    if comments == 1:
        r2 += 1
    if mathematica == 1:
        r2 += 1
    if formulas == 1:
        r2 += 1
    if maple == 1:
        r2 += 1
    if other == 1:
        r2 += 1



    if r2 > 4:
        r2 = 4
    result[0,1] = r2
    return result

def prime():
    filename_old = 'isPrime_v1.csv'
    isData = loadArray(filename_old)
    single_col = np.zeros([342305,2])

    for oeis_id in range(max(np.shape(isData))):
        assert isData[oeis_id, 0] == oeis_id

        single_col[oeis_id,:] = primeDecision(isData[oeis_id,1:])

    return single_col

def contFracDecision(columns):
    cofr = columns[0]
    nameConvergents = columns[1]
    name = columns[2]
    mathematica = columns[3]

    r1 = r2 = 0
    result = np.zeros([1,2])
    if cofr == 1:
        r1 += 4

    if nameConvergents == 1:
        r2 += 4
    if name == 1:
        r1 += 3
        r2 += 4
    if mathematica == 1:
        r2 += 3

    if r2 > 4:
        r2 = 4
    if r1 > 4:
        r1 = 4
    result[0,0] = r1
    result[0,1] = r2

    return result

def contFrac():
    filename_old = 'isContinuedFraction_v1.csv'
    isData = loadArray(filename_old)
    single_col = np.zeros([342305,2])

    for oeis_id in range(max(np.shape(isData))):
        assert isData[oeis_id, 0] == oeis_id

        single_col[oeis_id,:] = contFracDecision(isData[oeis_id,1:])

    return single_col


def tablDecision(columns):
    tabl = columns[0]
    name = columns[1]
    comments = columns[2]
    formula = columns[3]

    r1 = r2 = 0

    if tabl == 1:
        r1 += 4

    if name == 1:
        r2 += 4
    if comments == 1:
        r2 += 2
    if formula == 1:
        r2 += 3

    if r2 > 4:
        r2 = 4
    if r1 > 4:
        r1 = 4
    result = np.zeros([1,2])
    result[0,0] = r1
    result[0,1] = r2

    return result

def tabl():
    filename_old = 'istwoD_v1.csv'
    isData = loadArray(filename_old)
    single_col = np.zeros([342305,2])

    for oeis_id in range(max(np.shape(isData))):
        assert isData[oeis_id, 0] == oeis_id

        single_col[oeis_id,:] = tablDecision(isData[oeis_id,1:])

    return single_col

def roundDecision(columns):
    name = columns[0]
    mathematica = columns[1]
    formula = columns[2]

    result = 0

    if name == 1:
        result += 3
    if formula == 1:
        result += 4
    if mathematica == 1:
        result += 4

    if result >4:
        result = 4

    return result

def rounding():
    filename_old = 'isRounded_v1.csv'
    isData = loadArray(filename_old)
    single_col = np.zeros([342305,1])

    for oeis_id in range(max(np.shape(isData))):
        assert isData[oeis_id, 0] == oeis_id

        single_col[oeis_id,:] = roundDecision(isData[oeis_id,1:])

    return single_col

def rootDecision(columns):
    """
    name = columns[0]
    mathematica = columns[1]
    formula = columns[2]
    name_string = columns[3]
    name_formula = columns[4]
    mathematica_formula = columns[5]
    formula_formula = columns[6]
    """
    result = 0
    s = np.count_nonzero(columns[:] == 1) - np.count_nonzero(columns[3] == 1)
    if s > 0:
        result = s + 1

    if result >4:
        result = 4

    return result

def roots():
    filename_old = 'isRoot_v1.csv'
    isData = loadArray(filename_old)
    single_col = np.zeros([342305,1])

    for oeis_id in range(max(np.shape(isData))):
        assert isData[oeis_id, 0] == oeis_id

        single_col[oeis_id,:] = rootDecision(isData[oeis_id,1:])

    return single_col


def sumOfSequencesDecision(columns):
    name_sum_of_seq = columns[0]
    formula_sum_of_seq = columns[1]
    name_seq_and_const = columns[2]
    formula_seq_and_const = columns[3]


    r1 = 0
    if name_sum_of_seq == 1 or formula_sum_of_seq == 1:
        r1 = 4
    r2 = 0
    if name_seq_and_const == 1 or formula_seq_and_const == 1:
        r2 = 4

    if r1 > 4:
        r1 = 4
    if r2 > 4:
        r2 = 4

    return np.array([r1,r2])

def sumOfSequences():
    filename_old = 'is_simple_sum_v2.csv'
    isData = loadArray(filename_old)
    single_col = np.zeros([342305,2])

    for oeis_id in range(max(np.shape(isData))):
        assert isData[oeis_id, 0] == oeis_id

        single_col[oeis_id,:] = sumOfSequencesDecision(isData[oeis_id,1:])

    return single_col

#print("id: " + str(oeis_id) + ",data: " + str(isData[oeis_id,1:]))


# title: oeis_id,polynomial,periodic,exponential,decimal expansion,expansion,fibonacci-like,consists of palindromes,palindrome related,consists of primes,prime related,is a continued fraction, related to continued fractions, is two-dimensional, related to two dimensional, is rounded, contains roots, sum of sequences, sum/product of sequence and constant
def main():
    filename = "combined_results_v3.csv"
    combined_results = np.zeros([342305,19])

    for oeis_id in range(342305):
        combined_results[oeis_id,0] = oeis_id

    results = [poly(),period(),exponential(),decimalExpansion(),expansion(),fibonacci(),palindrome(),prime(),contFrac(),tabl(),rounding(),roots(),sumOfSequences()]

    index = 1
    for r in results:
        dim = min(np.shape(r))
        combined_results[:,index:index+dim] = r[:,0:dim]
        index += dim

    header = "oeis_id,polynomial,periodic,exponential,decimal expansion,expansion,fibonacci-like,consists of palindromes,palindrome related,consists of primes,prime related,is a continued fraction, related to continued fractions, is two-dimensional, related to two dimensional, is rounded, contains roots, sum of sequences, sum/product of sequence and constant"

    saveArray(combined_results, filename, header)

def count_non_classified():
    filename = "combined_results_v3.csv"
    combined_results = loadArray(filename ,1)

    count = 0
    for oeis_id in range(342305):
        if np.count_nonzero(combined_results[oeis_id,1:] == 4) == 0 and np.count_nonzero(combined_results[oeis_id,1:] == 3) == 0:
            count += 1
    return count

def calculate_overview():
    filename = "combined_results_v3.csv"
    overview = np.zeros([5,19],dtype = int)
    first_col = np.arange(5)
    overview[:,0] = first_col
    my_header = "how sure we are,polynomial,periodic,exponential,decimal expansion,expansion,fibonacci-like,consists of palindromes,palindrome related,consists of primes,prime related,is a continued fraction, related to continued fractions, is two-dimensional, related to two dimensional, is rounded, contains roots, sum of sequences, sum/product of sequence and constant"

    data = loadArray(filename, skip = 1)

    for i in range(5):
        overview[i,1:] = np.count_nonzero(data[:,1:] == i, axis = 0)


    np.savetxt("overview.csv", overview.astype(int), fmt='%u', delimiter=',', header=my_header, comments="")
    #return overview
