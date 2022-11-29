from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

X = np.loadtxt('data\input_cleaned\wea_input.csv', skiprows=1, delimiter=',', usecols=range(1, 14))
y = np.loadtxt(r'data\input_cleaned\rad_input.csv', skiprows=1, delimiter=',', usecols=range(1, 14))

for i in [X, y]:
    print(type(i), i.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=1)
# Consider scaling data

# Test different activation functions
reg = MLPRegressor(hidden_layer_sizes=(64), activation='relu', random_state=1, max_iter=1000).fit(X_train, y_train)
pred = reg.predict(X_test)
print(pred)
print(pred.shape)
acc = reg.score(X_test, y_test)
print(acc)