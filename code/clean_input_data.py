"""
DESCRIPTION
"""

import pandas as pd



def read_data(file_dir):
    """
    This function reads in .csv data and outputs a pandas df.
    The date input must be named exatly as follows:
    date: 'DATE (MM/DD/YYYY)'
    time: 'MST'
    INPUT - .csv file
    OUTPUT - pandas df
    """
    df = pd.read_csv(file_dir, parse_dates=[['DATE (MM/DD/YYYY)', 'MST']])
    print(df)
    return df


# def merge_df():


def main():
    # DATA INPUT
    # rad_dir = 
    # every mins
    wea_dir = "/Volumes/GoogleDrive/My Drive/COURSES/22 AU/CSE_583/final_prj/data/raw/2020/2020_wea.csv"
    # every 30 mins (12:15, 12:45) --> round to nearest hour (12:00, 1:00)
    precip_water_dir = "../data/raw/2020_precipitable_water.csv"
    # every 10 mins (12:10, 12:20, 12:30)
    aod_dir = "/Volumes/GoogleDrive/My Drive/COURSES/22 AU/CSE_583/final_prj/data/raw/2020/2020_aod_ssa_asymmetry.csv"


    # wea_df = read_data(wea_dir)
    prcp_wtr_df = read_data(precip_water_dir)
    # aod_df = read_data(aod_dir)

    # Precip_wtr data has time series every 15mins and 45mins. 
    # This doesn't align with other data time series (i.e. aod - given every 10, 20, 30 etc mins).
    # So, we need to round the time to nearest hour.
    print(prcp_wtr_df)
    prcp_wtr_df['DATE (MM/DD/YYYY)_MST'] = prcp_wtr_df['DATE (MM/DD/YYYY)_MST'].dt.ceil(freq='30T')
    print(prcp_wtr_df)
    



if __name__ == "__main__":
    main()
