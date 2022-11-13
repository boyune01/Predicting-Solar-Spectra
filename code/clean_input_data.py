"""
This module is used to read in weather and solar spectra data
(downloaded from NREL website as .csv files) and cleans them
so that it's ready to be used for ML algorithms.
The functions in this module perform the following tasks:
(1) specifc for weather data - Read in multiple .csv data and convert to one pandas dataframe by concatenating them.
(2) Checking and removing rows with duplicate dates and NaN.
(3) Cull rows of data based on matching timeseries of multiple dataframes.
(4) specifc for solar spectra data - Read in multiple .csv data and convert to one pandas dataframe by concatenating them.
(5) For solar spectra data only - clean data into 1nm wavelength intervals by interpolating between measured wavelengths.
(6) Save cleaned pandas dataframes to .csv file.
"""

import pandas as pd
import os


def read_wea_datas(file_dir, identifier):
    """
    Function to read multiple .csv datas and merge them into 1 pandas df
    INPUT:
    (1) file_dir - directory of .csv files to read and combine in a pandas df.
    (2) identifier - part of file name that is repeated across all the files. 
    i.e. for files (rad_2018, rad_2019, rad_2020), identifier is 'rad'.
    OUTPUT:
    combined and sorted (based on datetime) pandas df.
    """
    files = os.listdir(file_dir)
    files = sorted(files)

    count = 0
    frames = []
    for file in files:
        count += 1
        if file.startswith(identifier):
            name = identifier + "_" + "df" + str(count)
            name = pd.read_csv(file_dir + file, on_bad_lines="skip", dtype="float", header=0, parse_dates=[['DATE (MM/DD/YYYY)', 'MST']])
            frames.append(name)
            
    # combine all csv monthly data into a pandas df
    if len(frames) > 1:
        combined_df = pd.concat(frames)  # if there is multiple frames, concat
    else:
        combined_df = name
    
    # Change name of the date column
    combined_df.rename(columns={'DATE (MM/DD/YYYY)_MST':'date'}, inplace = True)

    return combined_df


def drop_dup_nan(df, column):
    """
    Removes duplicates and NaNs from dataframe
    """
    print (f'Original dataframe: {len(df)} rows')

    df_dedup = df.drop_duplicates(subset=column)
    print (f'De-duplicated dataframe: {len(df_dedup)} rows')
    print (f'Duplicate entries: {len(df) - len(df_dedup)} rows')
    
    df_dedup_is_nan = df_dedup.isnull()  # [25000, 8]
    mask = df_dedup_is_nan.sum(axis=1) == 0  # [25000]

    df_dedup_no_nan = df_dedup[mask]  # [10000]
    
    print (f'Entries without NaN: {len(df_dedup_no_nan)}')
    print (f'Entries containing NaN: {len(df_dedup) - len(df_dedup_no_nan)}')
    
    return df_dedup_no_nan


def merge_df(*dataframes):
    """
    For this to work, all df must have atleast 1 column
    with same name (which is the column used to merge).
    This function will check for same data from the column
    and if it doens't match, those rows will be culled.
    """
    
    assert len(dataframes) > 1  # this raises error when there is only 1 df
    # 1st element of the list
    df = dataframes[0]
    
    # Remainder of the list (start from 1-th index, and onwards)
    for new_df in dataframes[1:]:
        df = df.merge(new_df, how='inner')
    return df


def read_rad_datas(file_dir, identifier):
    """
    Function to read multiple .csv datas and merge them into 1 pandas df
    INPUT:
    (1) file_dir - directory of .csv files to read and combine in a pandas df.
    (2) identifier - part of file name that is repeated across all the files. 
    i.e. for files (rad_2018, rad_2019, rad_2020), identifier is 'rad'.
    OUTPUT:
    combined and sorted (based on datetime) pandas df.
    """
    files = os.listdir(file_dir)
    files = sorted(files)

    count = 0
    frames = []
    for file in files:
        count += 1
        if file.startswith(identifier):
            name = identifier + "_" + "df" + str(count)
            name = pd.read_csv(file_dir + file, on_bad_lines="skip", dtype="float", header=None)
            frames.append(name)
            
    # combine all csv monthly data into a pandas df
    if len(frames) > 1:
        combined_df = pd.concat(frames)  # if there is multiple frames, concat
    else:
        combined_df = name

    return combined_df


def interpolation_1nm(df, wv_len_range):
    """
    This is a function to interpolate calibrated spectral data to 1nm interval
    INPUT:
    (1) pandas df containing only the wavelength data (no date / or any other information)
    (2) wv_len_range (list) - i.e. [334, 1076].
    OUTPUT - pandas dataframe interpolated (in 1nm interval)
    """
    # CONVERT TO 1NM INTERVALS USING INTERPOLATION
    full_wvlen = [float(x) for x in range(wv_len_range[0], wv_len_range[1])] # create full_wvlen range

    df.columns = df.columns.astype('float32') # change orig_wvlen df header to float from str
    orig_wvlen = df.columns.values.tolist()  # get orig_wvlen in to a list

    # remove dup wv len from full_wvlen based on orig_wvlen list
    nondup_full_wvlen = []
    for i in full_wvlen:
        if i not in orig_wvlen:
            nondup_full_wvlen.append(i)

    comb_wvlen = nondup_full_wvlen + orig_wvlen  # combine 1nm and orig wv_len into a list
    comb_wvlen.sort() # sort combined wvlen

    # create empty dataframe w full wv_len
    df1 = pd.DataFrame(columns=nondup_full_wvlen, index=df.index)

    # concatenate empty dataframe with original dataframe
    df = pd.concat([df, df1], axis=1, verify_integrity=True)

    # reorder the dataframe so wvlen is sorted
    df = df.loc[:, comb_wvlen]

    # change dtype from object to numerical (required for df.interpolate)
    df = df.astype('float32')

    # Interpolate
    df = df.interpolate(method='linear', axis=1)

    # get 1nm data only
    df = df.loc[:, full_wvlen[1:]]

    return df


def save_df_to_csv(df, file_dir):
    df.to_csv(file_dir, index=False)


def main():
    # DATA INPUT 
    # Directory containing all data inputs
    data_dir = "/Volumes/GoogleDrive/My Drive/COURSES/22 AU/CSE_583/final_prj/data/raw/"

    wv_len_dir = "../data/ref/rad_wvlen.csv"

    # READ AND CLEAN WEATHER DATA INPUT
    # Weather Data
    wea_df = read_wea_datas(data_dir, 'wea')
    wea_df = drop_dup_nan(wea_df, 'date')

    # Aerosol Optical Depth Data
    aod_df = read_wea_datas(data_dir, 'aod')
    aod_df = drop_dup_nan(wea_df, 'date')

    # Precipitable Water Content Data
    prcp_wtr_df = read_wea_datas(data_dir, 'precip')
    prcp_wtr_df["date"] = prcp_wtr_df["date"].dt.ceil(freq="30T")  # 12:15, 12:45 --> 12:00, 12:30
    prcp_wtr_df = drop_dup_nan(prcp_wtr_df, 'date')

    # Merge all df to have same time (= cull times when there aren't other data)
    input_df = merge_df(wea_df, prcp_wtr_df, aod_df)

    # READ AND CLEAN RADIATION DATA
    # format date
    rad_df = read_rad_datas(data_dir, "rad")
    rad_df["date"] = rad_df[1]*10000000 + rad_df[2]*10000 + rad_df[3]  # 20200010725
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
    measured_wv_len_num = measured_wv_len_df[0].values.tolist()  # get values of 1st col as list (to be used as new column)
    measured_wv_len_num.append('date')  # add date to the end
    rad_df.columns = measured_wv_len_num  # rename columns to match the wv_len_num

    # interpolate
    rad_df1 = rad_df.drop(columns=['date'], axis =1)  # part of df for spectrum (drop date column)
    interpolated_df = interpolation_1nm(rad_df1, [334, 1076])
    interpolated_df['date'] = rad_df['date']  # add back in date (contains date and spectral data in every 1nm)

    # Cull Radiation data based on same date time as input weather data:
    # Create 1 column df with just date
    date_df = input_df['date']  # get dates from input_df
    date_df = date_df.to_frame()  # make series to df

    rad_df3 = merge_df(date_df, interpolated_df)  # culled


    # DATA OUTPUT
    wea_out_dir = "../data/cleaned/2020_wea_input.csv"
    rad_out_dir = "../data/cleaned/2020_rad_input.csv"

    # Save
    save_df_to_csv(input_df, wea_out_dir)
    save_df_to_csv(rad_df3, rad_out_dir)


if __name__ == "__main__":
    main()
