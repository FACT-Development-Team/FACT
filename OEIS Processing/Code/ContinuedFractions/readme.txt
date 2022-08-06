infos about the file "isContinuedFraction_v1.csv"

Do not open the file in excel, values are not correcly displayed

To load the file in python use:
	import numpy as np
	isPoly = np.loadtxt('isContinuedFraction_v1.csv', delimiter=',')

First column: 	oeis_id of the sequence in question
Second column: 	sequence has keyword "cofr"
		0 = not True
		1 = True
		4 = sequence name is None, or has no elements
Third column: 	name has "continued fraction convergents" in it
		0 = not True
		1 = True
		4 = sequence keyword is None, or has no elements
Fourth column: 	name has "continued fraction" (but not as part of "continued fraction convergents")  in it
		0 = not True
		1 = True
		4 = sequence keyword is None, or has no elements
Fifth column: 	mathematica has "continued fraction"  or "continuedfraction" in it
		0 = not True
		1 = True
		4 = sequence comments is None, or has no elements
