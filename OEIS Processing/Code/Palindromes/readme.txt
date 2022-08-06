infos about the file "isPalindrome_v1.csv"

Do not open the file in excel, values are not correcly displayed

To load the file in python use:
	import numpy as np
	isPoly = np.loadtxt('isPalindrome_v1.csv', delimiter=',')

First column: 	oeis_id of the sequence in question
Second column: 	elements in sequence are all palindromes
		0 = not True
		1 = True
		4 = sequence is None or empty
Third column: 	name contains "palindrome" 
		0 = not True
		1 = True
		4 = name is None or empty
Fourth column: 	comments contains "palindrome" 
		0 = not True
		1 = True
		4 = comments is None or empty
Fifth column: 	mathematica programs contain "palindrome"
		0 = not True
		1 = True
		4 = mathematica programs is None or empty
Sixth column: 	keywords contain "base"
		0 = not True
		1 = True
		4 = keywords is None or empty

