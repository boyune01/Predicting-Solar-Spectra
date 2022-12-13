"""
This module is designed to run linear regressions of wea inputs on cct
cct is designated as vector y, wea inputs as matrix X
regression analysis performed using statsmodels
"""

import pandas as pd
import statsmodels.api as sm

pd.set_option('display.max_columns', None)

# reading in data and defining X matrix & y vector
df = pd.read_csv('../../data/input_cleaned/linreg.csv')
print(df)

X = df[['Zenith Angle [degrees]', 'Azimuth Angle [degrees]',
        'Total Cloud Cover [%]', 'Opaque Cloud Cover [%]',
        'AOD [400nm]', 'AOD [500nm]', 'AOD [675nm]',
        'AOD [870nm]', 'AOD [1020nm]', 'SSA [675nm]',
        'Asymmetry [675nm]',
        'Precipitable Water [mm]']]
y = df['cct']


"""
statsmodels approach
returns table of results including params and significance
as well as general evaluations of regression fitness
prints results and creates 'results' as dataframe
"""

X2 = sm.add_constant(X)
est = sm.OLS(y, X2)
est2 = est.fit()
print(est2.summary())

print('')
results = (est2.summary().tables[1])
print(results)