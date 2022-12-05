'''
This module is designed to run ridge regressions of wea inputs on cct
cct is designated as vector y, wea inputs as matrix X
regression analysis performed using sklearn
'''

import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import train_test_split

df = pd.read_csv('../../data/input_cleaned/linreg.csv')

X = df[['Zenith Angle [degrees]', 'Azimuth Angle [degrees]',
        'Total Cloud Cover [%]', 'Opaque Cloud Cover [%]',
        'AOD [400nm]', 'AOD [500nm]', 'AOD [675nm]',
        'AOD [870nm]', 'AOD [1020nm]', 'SSA [675nm]',
        'Asymmetry [675nm]',
        'Precipitable Water [mm]']]
y = df['cct']

alpha_range = np.arange(0, 10.0, 0.1)
clf_all_score = []

for i in alpha_range:
    clf = Ridge(alpha = i)
    clf.fit(X, y)
    clf_all_score.append(clf.score(X, y))

print('Max value :', max(clf_all_score))
print('Alpha :', alpha_range[clf_all_score.index(max(clf_all_score))])

clf = Ridge(alpha = alpha_range[clf_all_score.index(max(clf_all_score))])
clf.fit(X, y)

print('')
print('Intercept Coefficient')
print(clf.intercept_)
print('')

print('Coefficient Matrix')
cdf = pd.DataFrame(clf.coef_, X.columns, columns=['Coefficients'])
print(cdf)
print('')

print('R-Squared (i.e. measure of fit)')
print(clf.score(X, y))
print('')
