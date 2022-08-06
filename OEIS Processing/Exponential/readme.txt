infos about the file "is_Exponential.csv"

Do not open the file in excel, values are not correcly displayed

To load the file in python use:
	import numpy as np
	isPoly = np.loadtxt('is_Exponential.csv', delimiter=',')

First column: 	oeis_id of the sequence in question
Second column: 	Evaluation of the exponential behaviour
		0 = no exponential behaviour observed
		1 = sequence of quotients of subsequent elements aproach a fixed value (likely to be exponential)
		2 = sequence of quotients of subsequent elements seem to slowly aproach a fixed value (possible to be exponential)
		3 = sequence of given numbers not long enough to reach a conclusion
		4 = sequence is None, or has no elements
		5 = sequence is marked with "fini" or "dead" by oeis
		6 = quotients between subsequent elements could not be calculated
		7 = OverflowError when calculation quotients between subsequent elements, this Error is thrown when dividing by zero. 
		We don't handle this Error differently because exponential sequences are not likely to have a 0 (except at the beginning).
