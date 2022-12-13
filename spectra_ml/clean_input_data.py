"""
This module is used to read in weather and solar spectra data
(downloaded from NREL website as .csv files) and cleans them
so that it's ready to be used for ML algorithms.
The functions in this module perform the following tasks:
(1) specifc for weather data - Read in multiple .csv data
and convert to one pandas dataframe by concatenating them.
(2) Checking and removing rows with duplicate dates and NaN.
(3) Cull rows based on matching timeseries of 2 dataframes.
(4) specifc for solar spectra data - Read in multiple .csv data
and convert to one pandas dataframe by concatenating them.
(5) For solar spectra data only - clean data into 1nm wavelength
intervals by interpolating between measured wavelengths.
(6) Save cleaned pandas dataframes to .csv file.
"""
import os

import numpy as np
import pandas as pd


def read_wea_datas(file_dir, identifier):
    """
    Function to read multiple .csv datas and merge them into 1 pandas df.
    INPUT:
    (1) file_dir - directory of .csv files to read and combine in a pandas df.
    (2) identifier - part of file name that is repeated across all the files.
    i.e. for files (rad_2018, rad_2019, rad_2020), identifier is 'rad'.
    OUTPUT:
    combined and sorted (based on datetime) pandas df.
    """
    files = os.listdir(file_dir)
    files = sorted(files)

    # Check files are .csv
    for file in files:
        if not file.endswith(".csv"):
            raise ValueError("File type should be .csv")

    count = 0
    frames = []
    for file in files:
        count += 1
        if file.startswith(identifier):
            name = identifier + "_" + "df" + str(count)
            name = pd.read_csv(
                file_dir + file,
                on_bad_lines="skip",
                dtype="float",
                header=0,
                parse_dates={"date": ["DATE (MM/DD/YYYY)", "MST"]}
                )
            frames.append(name)

    # combine all csv monthly data into a pandas df
    if len(frames) > 1:
        combined_df = pd.concat(frames)  # if there is multiple frames, concat
    else:
        combined_df = identifier + "_" + "df"

    return combined_df


def drop_dup_nan(df, column):
    """
    Removes duplicates and NaNs from dataframe
    INPUT:
    (1) df (pandas dataframe) - dataframe to test for duplicates and NaNs.
    (2) column (string) - column in the dataframe to test for duplicates.
    OUTPUT: pandas dataframe
    """
    print(f"Original dataframe: {len(df)} rows")

    df_dedup = df.drop_duplicates(subset=column)
    print(f"De-duplicated dataframe: {len(df_dedup)} rows")
    print(f"Duplicate entries: {len(df) - len(df_dedup)} rows")

    df_dedup_is_nan = df_dedup.isnull()  # [25000, 8]
    mask = df_dedup_is_nan.sum(axis=1) == 0  # [25000]

    df_dedup_no_nan = df_dedup[mask]  # [10000]

    print(f'Entries without NaN: {len(df_dedup_no_nan)}')
    print(f'Entries containing NaN: {len(df_dedup) - len(df_dedup_no_nan)}')

    return df_dedup_no_nan


def merge_df(*dataframes):
    """
    For this to work, all df must have atleast 1 column
    with same name (which is the column used to merge).
    This function will check for same data from the column
    and if it doens't match, those rows will be culled.
    INPUT: Any number of pandas dataframes
    OUTPUT: pandas dataframe
    """

    # Test - Check there are multiple dataframes
    if len(dataframes) <= 1:
        raise TypeError(
            "There should be more than 1 dataframe to perform merge"
            )
    # assert len(dataframes) > 1  # this raises error when there is only 1 df

    # 1st element of the list
    df = dataframes[0]

    # Remainder of the list (start from 1-th index, and onwards)
    for new_df in dataframes[1:]:
        df = df.merge(new_df, how='inner')
    return df


def read_rad_datas(file_dir, identifier):
    """
    Function to read multiple .csv datas and merge them into 1 pandas df.
    Radiation data should contain wavelength range between 380nm to 780nm.
    INPUT:
    (1) file_dir - directory of .csv files to read and combine in a pandas df.
    (2) identifier - part of file name that is repeated across all the files.
    i.e. for files (rad_2018, rad_2019, rad_2020), identifier is 'rad'.
    OUTPUT:
    combined and sorted (based on datetime) pandas df.
    """
    files = os.listdir(file_dir)
    files = sorted(files)

    # Check there is atleast 1 file
    if len(files) == 0:
        raise TypeError("There should be atleast 1 file to run this function")

    # Check files are .csv
    for file in files:
        # print(file)
        if not file.endswith(".csv"):
            raise ValueError("File type should be .csv")

    count = 0
    frames = []
    for file in files:
        count += 1
        if file.startswith(identifier):
            name = identifier + "_" + "df" + str(count)
            name = pd.read_csv(
                file_dir + file,
                on_bad_lines="skip",
                dtype="float",
                header=None
                )
            frames.append(name)

    # combine all csv monthly data into a pandas df
    if len(frames) > 1:
        combined_df = pd.concat(frames)  # if there is multiple frames, concat
    else:
        combined_df = identifier + "_" + "df"

    return combined_df


def interpolation_1nm(df, wv_len_range):
    """
    This is a function to interpolate calibrated spectral data to 1nm interval.
    INPUT:
    (1) df (pandas df) - containing only the wavelength data
    (no date / or any other information)
    (2) wv_len_range (list) - i.e. [334, 1076].
    OUTPUT - pandas dataframe interpolated (in 1nm interval)
    """

    # Check there is only wavelengh data (check dtype of each column == float)
    for i in df.dtypes:
        if i != float:
            raise TypeError(
                "File should only contain wavelength data of type float")

    # Check column names include 380 to 780 nm
    if wv_len_range[0] > 380 or wv_len_range[1] < 780:
        raise ValueError(
            "File should contain wavelengths inbetween 380 to 780nm")

    # Convert to 1nm intervals using interpolation
    # create full_wvlen range
    full_wvlen = [float(x) for x in range(wv_len_range[0], wv_len_range[1])]

    # change orig_wvlen df header to float from str
    df.columns = df.columns.astype("float32")
    orig_wvlen = df.columns.values.tolist()  # get orig_wvlen in to a list

    # remove dup wv len from full_wvlen based on orig_wvlen list
    nondup_full_wvlen = []
    for i in full_wvlen:
        if i not in orig_wvlen:
            nondup_full_wvlen.append(i)

    # combine 1nm and orig wv_len into a list
    comb_wvlen = nondup_full_wvlen + orig_wvlen
    comb_wvlen.sort()  # sort combined wvlen

    # create empty dataframe w full wv_len
    df1 = pd.DataFrame(columns=nondup_full_wvlen, index=df.index)

    # concatenate empty dataframe with original dataframe
    df = pd.concat([df, df1], axis=1, verify_integrity=True)

    # reorder the dataframe so wvlen is sorted
    df = df.loc[:, comb_wvlen]

    # change dtype from object to numerical (required for df.interpolate)
    df = df.astype("float32")

    # Interpolate
    df = df.interpolate(method='linear', axis=1)

    # get 1nm data only
    df = df.loc[:, full_wvlen[1:]]

    return df


def cull_df(df1, df2):
    """
    Cull a dataframe based on time stamp of another dataframe.
    For this function to work, reference dataframe (df2) must
    have a column called 'date'.
    INPUT:
    (1) df1 (pandas df) - dataframe to cull
    (2) df2 (pandas df) - dataframe to reference time stamp
    OUTPUT:
    pandas dataframe
    """
    # Check there is time stamp (column for date)
    if len(df1.select_dtypes(include=[np.datetime64])) == 0:
        raise TypeError("Dataframe should include datetime dtype")

    # Check there is column name 'date'
    col_name1 = list(df1.columns.values)
    col_name2 = list(df2.columns.values)

    if "date" not in col_name1 or "date" not in col_name2:
        raise ValueError(
            "Dataframes should include column named 'date'")

    # create a df with just dates (from 'date' column of df2)
    date_df = df2["date"]
    date_df = date_df.to_frame()

    df = df1.merge(date_df, how='inner')

    return df


def save_df_to_csv(df, file_dir):
    df.to_csv(file_dir, index=False)


def main():
    # DATA INPUT
    # Directory containing all data inputs
    data_dir = "/Volumes/GoogleDrive/My Drive/COURSES/" \
               + "22 AU/CSE_583/final_prj/data/raw/"

    # READ AND CLEAN WEATHER DATA INPUT
    # Weather Data
    wea_df = read_wea_datas(data_dir, 'wea')
    wea_df = drop_dup_nan(wea_df, 'date')

    # Aerosol Optical Depth Data
    aod_df = read_wea_datas(data_dir, 'aod')
    aod_df = drop_dup_nan(aod_df, 'date')

    # Precipitable Water Content Data
    prcp_wtr_df = read_wea_datas(data_dir, 'precip')
    prcp_wtr_df["date"] = prcp_wtr_df["date"].dt.ceil(
        freq="30T")  # 12:15, 12:45 --> 12:00, 12:30
    prcp_wtr_df = drop_dup_nan(prcp_wtr_df, 'date')

    # Merge all df to have same time (cull times when there aren't other data)
    input_df = merge_df(wea_df, prcp_wtr_df, aod_df)

    # Check for negative values in weather data
    mask = input_df.loc[:, input_df.columns != 'date'] < 0
    mask1 = mask.sum(axis=1) <= 0
    input_df1 = input_df[mask1]
    input_df1

    # READ AND CLEAN RADIATION DATA
    # format date
    rad_df = read_rad_datas(data_dir, "rad")
    rad_df["date"] = rad_df[1]*10000000 + \
        rad_df[2]*10000 + rad_df[3]  # 20200010725
    rad_df["date"] = pd.to_datetime(rad_df["date"], format="%Y%j%H%M")

    # cull irrelevant columns
    time_idx = [x for x in range(0, 7)]
    other_idx = [x for x in range(1025, 1031)]
    drop_idx = time_idx + other_idx
    rad_df.drop(columns=drop_idx, inplace=True)

    # clean dup and NaN
    rad_df = drop_dup_nan(rad_df, 'date')

    # rename columns to match the measrued wavelength
    measured_wv_len_dir = "../data/ref/rad_wvlen.csv"
    measured_wv_len_df = pd.read_csv(measured_wv_len_dir, header=None)
    # get values of 1st col as list (to be used as new column)
    measured_wv_len_num = measured_wv_len_df[0].values.tolist()
    # add date to the end
    measured_wv_len_num.append("date")
    # rename columns to match the wv_len_num
    rad_df.columns = measured_wv_len_num

    # interpolate
    # part of df for spectrum (drop date column)
    rad_df1 = rad_df.drop(columns=["date"], axis=1)
    interpolated_df = interpolation_1nm(rad_df1, [334, 1076])
    # add back in date (contains date and spectral data in every 1nm)
    interpolated_df["date"] = rad_df["date"]

    # re-order 'date' column to first column
    cols = interpolated_df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    interpolated_df = interpolated_df[cols]

    # Cull both rad and weather data based on common datetime
    rad_df3 = cull_df(interpolated_df, input_df1)  # culled rad data
    input_df2 = cull_df(input_df1, rad_df3)  # culled wea data

    # DATA OUTPUT
    wea_out_dir = "../data/input_cleaned/wea_input.csv"
    rad_out_dir = "../data/input_cleaned/rad_input.csv"

    # Save
    save_df_to_csv(input_df2, wea_out_dir)
    save_df_to_csv(rad_df3, rad_out_dir)


if __name__ == "__main__":
    main()
