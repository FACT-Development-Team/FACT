infos about the file "isPrime_v1.csv"

Do not open the file in excel, values are not correcly displayed

To load the file in python use:
	import numpy as np
	isPoly = np.loadtxt('isPrime_v1.csv', delimiter=',')

First column: 	oeis_id of the sequence in question
Second column: 	elements are all primes
		0 = not True
		1 = True
		4 = name is None or empty
		8 = numbers are too big to calculate primality quick
Third column: 	name contains "prime" 
		0 = not True
		1 = True
		4 = name is None or empty
Fourth column: 	mathematica programs contains "prime" 
		0 = not True
		1 = True
		4 = is None or empty
Fifth column: 	comments contains "prime" 
		0 = not True
		1 = True
		4 = is None or empty
Sixth column: 	formulas contains "prime" 
		0 = not True
		1 = True
		4 = is None or empty
Seventh column: maple programs contains "prime" 
		0 = not True
		1 = True
		4 = is None or empty
Eight column: 	other programs contains "prime" 
		0 = not True
		1 = True
		4 = is None or empty
