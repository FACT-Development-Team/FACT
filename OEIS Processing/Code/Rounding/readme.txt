infos about the file "isRounded_v1.csv"

Do not open the file in excel, values are not correcly displayed

To load the file in python use:
	import numpy as np
	isPoly = np.loadtxt('isRounded_v1.csv', delimiter=',')

First column: 	oeis_id of the sequence in question
Second column: 	name contains any of ["rounded","rounding", "ceiling", "floor"]
		0 = not True
		1 = True
		4 = keywords is None or empty
Third column: 	mathematica contains any of ["round", "ceil", "floor"].
		0 = not True
		1 = True
		4 = name is None or empty
Fourth column: 	formulas contains any of ["round", "ceil", "floor"].
		0 = not True
		1 = True
		4 = comments is None or empty
