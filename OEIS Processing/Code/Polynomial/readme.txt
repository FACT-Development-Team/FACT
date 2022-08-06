infos about the file "dividedDiffsPolyFullRun7.csv"

Do not open the file in excel, values are not correcly displayed

To load the file in python use:
	import numpy as np
	isPoly = np.loadtxt('dividedDiffsPolyFullRun7.csv', delimiter=',')

First column: 	oeis_id of the sequence in question
Second column: 	Evaluation of the polynomial properties
		0 = could not fit a polynomial of degree <30
		1 = could fit a polynomial of degree <30 
		3 = sequence of given numbers not long enough to check wheter a fitted polynomial of degree n predicts at least another n elements
		4 = sequence is None, or has no elements
		5 = sequence is marked with "fini" or "dead" by oeis