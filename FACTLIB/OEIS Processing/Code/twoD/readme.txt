infos about the file "istwoD_v1.csv"

Do not open the file in excel, values are not correcly displayed

To load the file in python use:
	import numpy as np
	isPoly = np.loadtxt('istwoD_v1.csv', delimiter=',')

First column: 	oeis_id of the sequence in question
Second column: 	keywords contain "tabl"
		0 = not True
		1 = True
		4 = keywords is None or empty
Third column: 	name contains any of ["triangular array", "square array", "rectangular array", "triangle read by", "table read by", "matrix read by", "array read by"]
		0 = not True
		1 = True
		4 = name is None or empty
Fourth column: 	comments contains any of ["triangular array", "square array", "rectangular array", "triangle read by", "table read by", "matrix read by", "array read by"]
		0 = not True
		1 = True
		4 = comments is None or empty
Fifth column: 	formulas contains any of ["triangular array", "square array", "rectangular array", "triangle read by", "table read by", "matrix read by", "array read by"]
		0 = not True
		1 = True
		4 = formulas is None or empty
