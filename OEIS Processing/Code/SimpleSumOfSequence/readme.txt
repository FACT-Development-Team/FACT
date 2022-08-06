infos about the file "is_simple_sum_v2.csv"

Do not open the file in excel, values are not correcly displayed

To load the file in python use:
	import numpy as np
	isPoly = np.loadtxt('is_simple_sum_v2', delimiter=',')

First column: 	oeis_id of the sequence in question
Second column: 	name of sequence contains a sum of other oeis sequences for example: "a(n)=15*A052856(n+5)-423*A052856(n-21)+11*A123456(n)"
		0: False
		1: True
		4: name is None or empty
Third column:	formula of sequence contains a sum of other oeis sequences for example: "a(n)=15*A052856(n+5)-423*A052856(n-21)+11*A123456(n)"
		0: False
		1: True
		4: formula is None or empty
Fourth column:	name of sequence contains a sum/product/quotient of another sequence and a constant number for example: "A123456(n+1)-12" or "a(n)=A123456(n)/2"
		0: False
		1: True
		4: name is None or empty
Fifth column:	formula of sequence contains a sum/product/quotient of another sequence and a constant number for example: "A123456(n+1)-12" or "a(n)=A123456(n)/2"
		0: False
		1: True
		4: formula is None or empty
