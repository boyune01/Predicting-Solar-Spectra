"""
Module to check weather inputs for colinearity. Matrix X stores
the Weather. A pairplot function using seaborn allows for visual
assessment of data result.
"""

import pandas as pd
import seaborn as sns

pd.set_option('display.max_columns', None)


"""
reading in data and defining X matrix & y vector
"""

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
generate pairplot of explanatory variables
"""

sns.pairplot(X)
