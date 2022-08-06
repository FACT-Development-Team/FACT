import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold, train_test_split
from sklearn.linear_model import LinearRegression, Ridge, SGDRegressor, Lasso
from sklearn.preprocessing import PolynomialFeatures

#-------------- TRAIN_TEST_SPLIT --------------#

X = range(50)
y = [x**5 - x**2 for x in range(50)]
X_train, X_test, y1_train, y1_test = train_test_split(X, y, test_size=40, random_state=42) # Change second argument und choose different functions
X_train = np.reshape(X_train, (-1, 1))
X_test = np.reshape(X_test, (-1, 1))

#-------------- PREPROCESSING --------------#
MSE = []
Coefs = []
for i in range(0, 21):

    poly = PolynomialFeatures(degree=i)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.fit_transform(X_test)

    # model = SGDRegressor(alpha=0.2, learning_rate='adaptive', warm_start=True, max_iter=100000)
    model = LinearRegression()

    model.fit(X_train_poly, y1_train)
    Coefs.append(model.coef_)

    y1_pred = model.predict(X_test_poly)

    error1 = MSE.append(mean_squared_error(y1_test, y1_pred))

    print("Degree " + str(i) +  "\t" + str(MSE[i]))
    
#-------------- PRINT ERROR AND POLYNOMIAL --------------#

#print("\n Function: " + "6305 * x**3 - 18659 * x**2 + 12354 * x")

print("\n Best error with degree: " + str(MSE.index(min(MSE))))
poly = ""
min_index = MSE.index(min(MSE))
for i in range(len(Coefs[min_index]) - 1, 0, -1):
    if (np.abs(Coefs[min_index][i]) != 0):
        poly += str(Coefs[min_index][i]) + 'x[' + str(i) + "] + \n"
print("\n" + str(poly) + 'C')

#-------------- WRITE RESULTS TO FILE --------------#

#f = open('results1.csv', 'w')
#f.write("\n Best error with degree: " + str(MSE.index(min(MSE))))
#f.write("\n" +  str(min(MSE)))

#f.close()

#plt.scatter(range(100), generate_sequence(f3, 100))

#plt.plot(X_test, y1_pred, color='red', linewidth=3)