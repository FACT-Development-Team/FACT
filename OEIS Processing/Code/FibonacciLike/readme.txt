infos about the files "isFibonacci_v1.csv" and "fibonacci_formula_v1.csv"

a sequence being "fibonacci-like" refers to the existence of a formula of the form a(n) = d*a(n - d) + d*a(n - d) + ... where d refers to (different) integer values 

in "isFibonacci_v1.csv" :
First column: 	oeis_id of the sequence in question
Second column: 	0 = no fibonacci-like formula found in the sequence title
		1 = fibonacci-like formula found in the sequence title
Third column: 	0 = no fibonacci-like formula found in the "formula" section
		1 = fibonacci-like formula found in the "formula" section
		4 = sequence does not contain a formula section


in "fibonacci_formula_v1.csv" :
First column: 	oeis_id of the sequence in question
Second column: 	"" when the corresponding entry in "isFibonacci_v1.csv" is 0
		the found forumla in the sequence title when the corresponding entry in "isFibonacci_v1.csv" is 1
Third column: 	"" when the corresponding entry in "isFibonacci_v1.csv" is 0
		the found forumla in the formula section when the corresponding entry in "isFibonacci_v1.csv" is 1
