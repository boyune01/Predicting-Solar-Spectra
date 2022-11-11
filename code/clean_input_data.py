"""
This module ....
"""

import pandas as pd


def read_wea_data(file_dir):
    """
    This function reads in .csv data and outputs a pandas df.
    The date input must be named exatly as follows:
    date: 'DATE (MM/DD/YYYY)'
    time: 'MST'
    INPUT - .csv file
    OUTPUT - pandas df
    """
    df = pd.read_csv(file_dir, parse_dates=[['DATE (MM/DD/YYYY)', 'MST']])
    return df


def merge_df(*dataframes):
    """
    This function merges all the pandas df (input) and merge based on a column with same name.
    All input df must have 1 column with same name.
    If the data from the both columns match, that row will remain in the new df.
    INPUT - multiple pandas df
    OUTPUT - one pandas df
    Usage:
    df1 = ...
    df2 = ...
    df3 = ...
    merged_df = merge_df(df1, df2)
    merged_df2 = merge_df(df1, df2, df3)
    """
    assert len(dataframes) > 1  # this raises error when there is only 1 df
    # 1st element of the list
    df = dataframes[0]
    
    # Remainder of the list (start from 1-th index, and onwards)
    for new_df in dataframes[1:]:
        df = df.merge(new_df, how='inner')
    return df


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
    df.to_csv(file_dir)



def main():
    # DATA INPUT
    rad_in_dir = "/Volumes/GoogleDrive/My Drive/COURSES/22 AU/CSE_583/final_prj/data/raw/2020/2020_0102_rad.csv"

    wea_in_dir = "../data/raw/2020_wea.csv"  # every mins
    precip_water_in_dir = "../data/raw/2020_precipitable_water.csv"  # every 30 mins (12:15, 12:45)
    aod_in_dir = "../data/raw/2020_aod_ssa_asymmetry.csv"  # every 10 mins (12:10, 12:20, 12:30)

    wv_len_dir = "/Volumes/GoogleDrive/My Drive/COURSES/22 AU/CSE_583/final_prj/data/raw/rad_wvlen.csv"

    # Read Input Data
    wea_df = read_wea_data(wea_in_dir)
    prcp_wtr_df = read_wea_data(precip_water_in_dir)
    aod_df = read_wea_data(aod_in_dir)

    # Round time for prcp_wtr_df
    # Precip_wtr data has time series every 15mins and 45mins
    # which doesn't align with other data time series (i.e. aod - given every 10, 20, 30 etc mins)
    # So, we need to round the time to nearest hour
    prcp_wtr_df['DATE (MM/DD/YYYY)_MST'] = prcp_wtr_df['DATE (MM/DD/YYYY)_MST'].dt.ceil(freq='30T')

    # Merge all df to have same time (= cull times when there aren't other data)
    input_df = merge_df(wea_df, prcp_wtr_df, aod_df)

    # Rename input data (all weather data) date column (to be used when culling solar_rad data)
    input_df.rename(columns={'DATE (MM/DD/YYYY)_MST':'date'}, inplace = True)


    # Read Solar Spectral Data
    rad_df = pd.read_csv(rad_in_dir, header=None)

    # Create a date column with same timeseries format as input data
    # 1=yr, 2=month, 3=hour (726=7:26) 
    # need to make date into sth like 20200010725 and give format "%Y%j%H%M"
    rad_df["date"] = rad_df[1]*1000000 + rad_df[2]*1000 + rad_df[3]
    rad_df["date"] = pd.to_datetime(rad_df["date"], format="%Y%j%H%M")
    
    # cull irrelevant columns
    time_idx = [x for x in range(0, 7)]  # 1=yr, 2=month, 3=hour (726=7:26)
    other_idx = [x for x in range(1025, 1031)]
    drop_idx = time_idx + other_idx

    rad_df.drop(columns=drop_idx, inplace=True)
    
    # rename columns to match the measured wavelengths
    # Currently, it's just labeled numberically (0,1,2,3 ...)
    wv_len_df = pd.read_csv(wv_len_dir, header=None)
    new_col_name = wv_len_df[0].values.tolist()
    new_col_name.append('date')  # add date to the end of list containing new column names
    rad_df.columns = new_col_name  # rename columns to match the new column names

    # Create new df for interpolation (just to put into interpolation_1nm function)
    rad_df1 = rad_df.drop(columns=['date'], axis=1)

    # Interpolate to get data into every 1nm
    rad_df2 = interpolation_1nm(rad_df1, [334, 1076])

    # Add back in the date column to the interpolated spectral data
    rad_df2['date'] = rad_df['date']  # this contains date and spectral data in every 1nm

    # Cull Radiation data based on same date time as input weather data:
    # Create 1 column df with just date
    date_df = input_df['date']  # get date from input weather df
    date_df = date_df.to_frame()  # make series to df

    # Cull
    rad_df3 = merge_df(date_df, rad_df2)


    # DATA OUTPUT
    wea_out_dir = "../data/cleaned/2020_wea_input.csv"
    rad_out_dir = "../data/cleaned/2020_rad_input.csv"

    # Save
    save_df_to_csv(input_df, wea_out_dir)
    save_df_to_csv(rad_df3, rad_out_dir)



if __name__ == "__main__":
    main()
