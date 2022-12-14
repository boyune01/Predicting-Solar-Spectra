"""
Module to do the unittests.
"""
import numpy as np
import pandas as pd
import unittest

from spectra_ml import clean_input_data
from spectra_ml import calc_cct


rad_data_dir = "data/data_for_test/"
wea_data_dir = "data/input_example/2020_wea.csv"
precip_data_dir = "data/input_example/2020_precipitable_water.csv"
data_dir = "data/input_example/"


class UnitTests(unittest.TestCase):

    def test_read_wea_datas_smoke(self):
        """
        Smoke test to check the function runs.
        """
        clean_input_data.read_wea_datas(data_dir, 'wea')
        return

    def test_read_wea_datas_edge(self):
        """
        Edge test to test for .csv format
        """
        with self.assertRaises(ValueError):
            file_dir = "docs"
            clean_input_data.read_wea_datas(file_dir, 'wea')
        return

    def test_drop_dup_nun_smoke(self):
        """
        Smoke test to check the function runs.
        """
        df = pd.read_csv(
                wea_data_dir,
                parse_dates={"date": ["DATE (MM/DD/YYYY)", "MST"]}
                )
        clean_input_data.drop_dup_nan(df, 'date')
        return

    def test_merge_df_edge(self):
        """
        Check there are multiple dataframes.
        """
        with self.assertRaises(TypeError):
            df = pd.DataFrame()
            clean_input_data.merge_df(df)  # Only one dataframe
        return

    def test_read_rad_datas_smoke(self):
        """
        Smoke test to check the function runs.
        """
        clean_input_data.read_rad_datas(rad_data_dir, 'rad')
        return

    def test_read_rad_datas_edge(self):
        """
        Edge test to test for .csv format.
        """
        with self.assertRaises(ValueError):
            file_dir = "docs"
            clean_input_data.read_rad_datas(file_dir, 'rad')
        return

    def test_interpolation_1nm_edge1(self):
        """
        Edge test to check there is only wavelength data
        by checking columns names are float.
        """
        with self.assertRaises(TypeError):
            df = pd.DataFrame()
            df['date'] = ['2015-07-01 09:00:00',
                          '2015-07-01 10:00:00', '2015-07-01 11:00:00']
            df[334] = [0.000000, 0.000000, 0.000000]
            df[335.6] = [-0.008907, -0.003605, -0.004590]
            clean_input_data.interpolation_1nm(df, [380, 780])
        return

    def test_interpolation_1nm_edge2(self):
        """
        Edge test to check visible wavelength is included (380 to 780).
        """
        with self.assertRaises(ValueError):
            df = pd.DataFrame()
            df[388] = [0.000000, 0.000000, 0.000000]
            df[1076] = [-0.008907, -0.003605, -0.004590]
            clean_input_data.interpolation_1nm(df, [388, 1076])
        return

    def test_cull_df_smoke(self):
        """
        Smoke test to check there are 2 dataframes.
        """
        df1 = pd.read_csv(
                wea_data_dir,
                parse_dates={"date": ["DATE (MM/DD/YYYY)", "MST"]}
                )

        df2 = pd.read_csv(
                precip_data_dir,
                parse_dates={"date": ["DATE (MM/DD/YYYY)", "MST"]}
                )

        clean_input_data.cull_df(df1, df2)
        return

    def test_cull_df_edge1(self):
        """
        Edge test to check there is a column name "date".
        """
        with self.assertRaises(TypeError):
            df1 = pd.DataFrame()
            df2 = pd.DataFrame()
            clean_input_data.cull_df(df1, df2)
        return

    def test_cull_df_edge2(self):
        """
        Edge test to check there is time stamp (pandas datetime datatype).
        """
        with self.assertRaises(TypeError):
            df1 = pd.DataFrame()
            df2 = pd.DataFrame()
            clean_input_data.cull_df(df1, df2)
        return

    def save_df_to_csv_smoke(self):
        """
        Smoke test to check file_dir exists.
        """
        file_dir = ""
        df = pd.DataFrame()
        clean_input_data.save_df_to_csv(df, file_dir)
        return

    def cal_cct_smoke(self):
        """
        Smoke test to check the fuction run.
        """
        spectral_data = "data/input_cleaned/rad_input.csv"
        spd_df = pd.read_csv(spectral_data, header=0, index_col=0)
        cct_df = calc_cct.calc_cct(spd_df)
        save_dir = "../data/input_cleaned/cct_input.csv"
        cct_df.to_csv(save_dir)
        return

    def cal_cct_edge1(self):
        """
        Edge test to check the column names contain 380 to 780 nm.
        """
        with self.assertRaises(ValueError):
            df = pd.DataFrame()
            df[334] = [0.000000, 0.000000, 0.000000]
            df[335.6] = [-0.008907, -0.003605, -0.004590]
            calc_cct.calc_cct(df)
        return

    def cal_cct_edge2(self):
        """
        Edge test to check the interval 1 nm.
        """
        with self.assertRaise(ValueError):
            df = pd.DataFrame()
            df[334] = [0.000000, 0.000000, 0.000000]
            df[335.6] = [-0.008907, -0.003605, -0.004590]
            calc_cct.calc_cct(df)
        return

    def cal_cct_one_shot(self):
        """
        One-shot test to check CCT for a date.
        """
        spectral_data = "../data/input_cleaned/rad_input.csv"
        spd_df = pd.read_csv(spectral_data, header=0, index_col=0, nrows=1)
        assert np.isclose(calc_cct.calc_cct(spd_df), 5310.15)
        return
