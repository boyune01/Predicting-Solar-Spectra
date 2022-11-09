"""
DESCRIPTION
"""

import pandas as pd



def read_n_sort_wea(file_dir):
    """
    This function reads in weather data (which contains zenith angle, alzimuth angle, cloud cover, cloud cover opaque, pressue) in .csv format
    INPUT - .csv file
    OUTPUT - pandas df
    """
    df = pd.read_csv(file_dir, parse_dates=[['DATE (MM/DD/YYYY)', 'MST']])
    print(df)
    



def main():
    # DATA INPUT
    # rad_dir = 
    # every mins
    wea_dir = "/Volumes/GoogleDrive/My Drive/COURSES/22 AU/CSE_583/final_prj/data/raw/2020/2020_wea.csv"
    # every 30 mins (12:15, 12:45) --> round to nearest hour (12:00, 1:00)
    # prciptble_water_dir = 
    # every 10 mins (12:10, 12:20, 12:30)
    # aod_dir = 


    read_n_sort_wea(wea_dir)    


if __name__ == "__main__":
    main()
