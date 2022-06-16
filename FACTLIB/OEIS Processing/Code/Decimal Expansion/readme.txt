infos about the file "decimal_expansion.csv"

Do not open the file in excel, values are not correcly displayed

To load the file in python use:
	import numpy as np
	isPoly = np.loadtxt('dividedDiffsPolyFullRun7.csv', delimiter=',')

First column: 	oeis_id of the sequence in question
Second column: 	name has "decimal expansion" in it
		0 = not True
		1 = True
		4 = sequence name is None, or has no elements
Third column: 	sequence has keyword "cons"
		0 = not True
		1 = True
		4 = sequence keyword is None, or has no elements
Fourth column: 	sequence has keyword "base"
		0 = not True
		1 = True
		4 = sequence keyword is None, or has no elements
Fifth column: 	comments has "decimal expansion" in it
		0 = not True
		1 = True
		4 = sequence comments is None, or has no elements
