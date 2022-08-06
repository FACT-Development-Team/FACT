import read_logs
import matplotlib.pyplot as plt
from generate import *
import pandas as pd

results = read_logs.read_logs('../experiments')

# polynomials = set([run['polynomial'] for run in results])
# print(polynomials)

df = pd.DataFrame(results)
# df1 = df.loc[(df['polynomial'] == '2 * x + 5')]
# print(df1.sort_values(by='avg'))
df1 = df.loc[(df['polynomial'] == '(3 * x + 1) * (3 * x + 2)')]
print(df1.sort_values(by='avg'))
df2 = df.loc[(df['polynomial'] == 'x**10 - 1')]
print(df2.sort_values(by='avg'))
df3 = df.loc[(df['polynomial'] == '(x + 1) * (x + 2) * (x + 3)')]
print(df3.sort_values(by='avg'))

