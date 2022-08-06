# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 15:02:51 2021

@author: Emanuel
"""



start = r"a\(n\)="
integer = r"(\d+)"
shortfraction = r"\/\d+"
realfraction = r"\d+\/\d+"
parrealfraction = r"\(" + realfraction + r"\)"
monomial = r"((((\d+)|(\d+\*))*n(\^\d+)?)|" + integer + r")"
parmonomial = r"\(" + monomial + r"\)"
simppoly = monomial + r"([\+\-]" + monomial + r")*"
parsimppoly = r"\(" + simppoly + r"\)"

basicpoly = r"(" + parsimppoly + r"|" + simppoly + r")" #polynomials of the form 5*n^4 + 4n + 5 with or without parentesis
polyPower = r"(" + parsimppoly + r"\^\d+)"





"""
polySum = r"((" + basicpoly + r"|" + polyPower + r")([\+\-]" + basicpoly + r"|" + polyPower + r")+)"
polySumOptPar = r"(" + polySum + r"|(\(" + polySum + r"\)))" #optional parentesis

factor =  r"(" + polySumOptPar + r"|" + polyPower + r"|" + basicpoly + r"|" + realfraction + r"|" + r"|" + parrealfraction + r")"
polyProd = r"(" + factor + r"(((\*" + factor + r")+)|(" + shortfraction + r")))"
polyProdOptPar = r"(" + polyProd + r"|(\(" + polyProd + r"\)))" #optional parentesis

poly = r"((" + polyPower + r")|(" + simppoly + r")|(" + parsimppoly + r")|(" + polyProdOptPar + r"))([\+\-\*]" + r"((" + polyPower + r")|(" + simppoly + r")|(" + parsimppoly + r")|(" + polyProdOptPar + r")))*"
"""
#nice command to get the raw string back: print(r'%s' %poly)