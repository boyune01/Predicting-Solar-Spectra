"""
This module is designed to run ridge regressions of wea inputs on cct
cct is designated as vector y, wea inputs as matrix X
regression analysis performed using sklearn
"""
# %matplotlib inline

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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


"""
plot coefficient-alphas
"""


alpha_range = np.arange(0.1, 10.0, 0.1)
label_plot = ['Zenith Angle [degrees]', 'Azimuth Angle [degrees]',
              'Total Cloud Cover [%]', 'Opaque Cloud Cover [%]',
              'AOD [400nm]', 'AOD [500nm]', 'AOD [675nm]',
              'AOD [870nm]', 'AOD [1020nm]', 'SSA [675nm]',
              'Asymmetry [675nm]', 'Precipitable Water [mm]']

coefs = []
ridge = Ridge(normalize=True)
for a in alpha_range:
    ridge.set_params(alpha=a)
    ridge.fit(X, y)
    coefs.append(ridge.coef_)

np.shape(coefs)

ax = plt.gca()
ax.plot(alpha_range, coefs, label=label_plot)
plt.title('Ridge Regression')
plt.xlabel('Alpha')
plt.ylabel('Coefficients')
ax.legend(loc=1, fontsize=8)


"""
k fold cross validation (k = 5)
"""

"""
How to compute MSE?
Attributes cv_values_ is only available if store_cv_values=True and cv=None,
which are for  Leave-One-Out cross-validation
"""

alpha_range = np.arange(0.1, 10.0, 0.1)

train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2,
                                                    random_state=0)

regressor = RidgeCV(alphas=alpha_range, cv=5)
regressor.fit(train_X, train_y)


print('')
print('Intercept Coefficient')
print(regressor.intercept_)
print('')

print('Coefficient Matrix')
coeff_matrix = pd.DataFrame(regressor.coef_, X.columns,
                            columns=['Coefficients'])
print(coeff_matrix)
print('')

print('R-Squared (i.e. measure of fit)')
print(regressor.score(X, y))
print('')


"""
Train the ridge regression model with all data
Use for loop to find the best alpha value
"""


alpha_range = np.arange(0, 10.0, 0.1)
clf_all_score = []

for i in alpha_range:
    clf = Ridge(alpha=i)
    clf.fit(X, y)
    clf_all_score.append(clf.score(X, y))

print('Max value :', max(clf_all_score))
print('Alpha :', alpha_range[clf_all_score.index(max(clf_all_score))])

clf = Ridge(alpha=alpha_range[clf_all_score.index(max(clf_all_score))])
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
