"""
this module is designed to run linear regressions of wea inputs on cct
cct is dsignated as vector y, wea inputs as matrix X
regression analysis performed using statsmodels and sklearn
statsmodels approach seems to be better suited
"""

import pandas as pd
# import numpy as np

import statsmodels.api as sm
# from scipy import stats

from sklearn import linear_model

pd.set_option("display.max_columns", None)


"""
reading in data and defining X matrix & y vector
"""

# hey

df = pd.read_csv('~/Predicting-Sun-Spectra/data/input_cleaned/linreg.csv')
print(df)

X = df[["Zenith Angle [degrees]", "Azimuth Angle [degrees]",
        "Total Cloud Cover [%]", "Opaque Cloud Cover [%]",
        "AOD [400nm]", "AOD [500nm]", "AOD [675nm]",
        "AOD [870nm]", "AOD [1020nm]", "SSA [675nm]",
        "Asymmetry [675nm]",
        "Precipitable Water [mm]"]]
y = df["cct"]

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

print("")
results = (est2.summary().tables[1])
print(results)


"""
sklearn approach
prints regression coefficients as well as R-Squared
Not as thorough as statsmodels, I don't know why we'd use this
"""

regr = linear_model.LinearRegression()
regr.fit(X, y)

print("")
print("Intercept Coefficient")
print(regr.intercept_)
print("")

print("Coefficient Matrix")
cdf = pd.DataFrame(regr.coef_, X.columns, columns=['Coefficients'])
print(cdf)
print("")

print("R-Squared (i.e. measure of fit)")
print(regr.score(X, y))
print("")

"""
regr = linear_model.LinearRegression()
regr.fit(X, y)
params = np.append(regr.intercept_, regr.coef_)
predictions = regr.predict(X)

newX = pd.DataFrame({"Constant":np.ones(len(X))}).join(pd.DataFrame(X))
MSE = (sum((y-predictions)**2))/(len(newX)-len(newX.columns))

var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
sd_b = np.sqrt(var_b)
ts_b = params/ sd_b

p_values =[2*(1-stats.t.cdf(np.abs(i),
           (len(newX)-len(newX[0])))) for i in ts_b]

sd_b = np.round(sd_b, 3)
ts_b = np.round(ts_b, 3)
p_values = np.round(p_values, 3)
params = np.round(params, 4)

output = pd.DataFrame()
output["Coefficients"], output["Standard Errors"], output["T-Stat"],
                        output["p-value"] = [params, sd_b, ts_b, p_values]
print(output)
"""
