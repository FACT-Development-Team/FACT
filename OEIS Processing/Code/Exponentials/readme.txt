infos about the file "is_Exponential_v3.csv"

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
		8 = sequence of quotients of subsequent elements (seem) to aproach 1
		We don't handle this Error differently because exponential sequences are not likely to have a 0 (except at the beginning).
Third column:	Infos about the name of the sequence
		0 = nothing was found in the name
		1 = a pattern like "a(n) = *^(*n*)." was found in the name
		4 = name of sequence is None, or is empty #should not happen
Fourth column:	Infos about the formulas of the sequence
		0 = nothing was found in the formulas
		1 = a pattern like "a(n) = *^(*n*)." was found in the formulas
		4 = formulas of sequence is None, or is empty
Fifth column:	Infos about the mathematica_programs of the sequence
		0 = nothing was found in the mathematica_programs
		1 = a pattern like "Table[*^(*n*)]" was found
		4 = mathematica_programs of sequence is None, or is empty
