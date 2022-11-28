import pandas as pd

pd.set_option('display.max_columns', None)

df_wea = pd.read_csv("/home/bmcgreal/Predicting-Sun-Spectra/data/input_cleaned/wea_input.csv")
print(df_wea)

df_cct = pd.read_csv("/home/bmcgreal/Predicting-Sun-Spectra/data/input_cleaned/cct_input.csv")
print(df_cct)

df_linreg = pd.merge(df_wea, df_cct,
                     on='date',
                     how='inner')
print(df_linreg)

df_linreg.to_csv("/home/bmcgreal/Predicting-Sun-Spectra/data/input_cleaned/linreg.csv")
