infos about the files "isRoot_v1.csv" and "root_strings_v1.csv"



in "isRoot_v1.csv" :
column:		content:
#0: 		oeis_id
#1: 		name contains root but not rooted
#2: 		mathematica contains root but not rooted
#3: 		formulas contains root but not rooted
#4: 		name contains a string like: "square root" or "fifth-root" ,using the regex: (( )|(^))(([a-z]+)|(\d+th))(( )|(-))root 
#5: 		name contains a string like: "^(5/3)" or "^(n/8)", using the regex: ((\^\((n\/\d+)\))|(\^\((\d+\/\d+)\)))
#6:		mathematica contains a string like: "^(5/3)" or "^(n/8)", using the regex: ((\^\((n\/\d+)\))|(\^\((\d+\/\d+)\)))
#7:		formulas contains a string like: "^(5/3)" or "^(n/8)", using the regex: ((\^\((n\/\d+)\))|(\^\((\d+\/\d+)\)))

in every column the following code is used:
	0 = the statement is False
	1 = the statement is True
	4 = the respective field is None or empty

in "root_strings_v1.csv" :
column:		content:
#0: 		oeis_id
#1: 		contains the first word of the string found in index 4 of results
#2: 		contains the power in the string found in index 5 of results
#3: 		contains the power in the string found in index 6 of results
#4: 		contains the power in the string found in index 7 of results
