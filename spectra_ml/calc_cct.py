"""
Module to calculate Correlated Color Temperature (CCT).
"""

import pandas as pd
import numpy as np


def calc_cct(df):
    """
    Function to calculate CCT given a continuous spectral data.
    Input (pandas dataframe): Time series spectral data in every 1nm
    that contains wavelengths between 380nm to 780nm.
    Time series should be given as index, not a column.
    Output (pandas dataframe): Time series CCT data.
    """

    # Check column names include 380 to 780 nm
    required_nm = [str(float(x)) for x in range(380, 781)]
    if (not all(item in df for item in required_nm)):
        raise ValueError(
            "Columns should include wavelength range between 380-780nm"
            )

    # Check intervals are 1nm
    col_names = list(df.columns)  # each values as str
    col_names1 = [float(i) for i in col_names]  # put each values as float

    for i in (range(0, len(df)-1)):
        if (col_names1[i+1] - col_names1[i]) != 1:
            raise ValueError("Column interval should be 1nm")

    ciexyz_data = "../data/ref/cie_xyz.csv"
    xyz_df = pd.read_csv(ciexyz_data, index_col=0, header=9)
    xyz_df = xyz_df.transpose()
    # change index names to be in format '380.0'
    xyz_df.columns = [str(float(idx)) for idx in xyz_df.columns.to_list()]

    # Cull spectra to only 380nm to 780nm
    vis_wv = [str(float(x)) for x in range(380, 781)]
    df = df[vis_wv]

    x_val = xyz_df.loc['X_curve']
    y_val = xyz_df.loc['Y_curve']
    z_val = xyz_df.loc['Z_curve']

    df['CIE_X'] = df.mul(x_val, axis=1).sum(axis=1)*683
    df['CIE_Y'] = df.mul(y_val, axis=1).sum(axis=1)*683
    df['CIE_Z'] = df.mul(z_val, axis=1).sum(axis=1)*683

    df['XYZ_temp'] = df['CIE_X'] + df['CIE_Y'] + df['CIE_Z']
    df['x'] = df['CIE_X'] / df['XYZ_temp']
    df['y'] = df['CIE_Y'] / df['XYZ_temp']
    df['n'] = (df['x']-0.3366)/(df['y']-0.1735)

    df['cct'] = -949.86315 + (6253.80338 * np.exp(-df['n'] / 0.92159)) + (28.70599 * np.exp(-df['n'] / 0.20039)) + (0.00004*np.exp(-df['n'] / 0.07125))

    mask = df['cct'] >= 50000  # for CCT > 50,000K

    df1 = df[mask]
    df1['n'] = (df1['x']-0.3356) / (df1['y']-0.1691)
    df1['cct'] = 36284.48953 + (0.00228 * np.exp(-df1['n'] / 0.07861)) + (5.4535e-36 * np.exp(-df1['n'] / 0.01543))

    df.update(df1)
    df1 = df['cct']

    return df1


def main():
    """
    Definition to run the calc_cct function.
    """
    spectral_data = "../data/input_cleaned/rad_input.csv"
    spd_df = pd.read_csv(spectral_data, header=0, index_col=0)

    cct_df = calc_cct(spd_df)

    save_dir = "../data/input_cleaned/cct_input.csv"
    cct_df.to_csv(save_dir)


if __name__ == "__main__":
    main()
