"""
Test function
"""
import unittest
import pandas as pd
from code import clean_input_data

# data_dir = "/Volumes/GoogleDrive/My Drive
# /COURSES/22 AU/CSE_583/final_prj/data/raw/"
rad_data_dir = "../../data/data_for_test/test_rad_df.csv"
wea_data_dir = "../../data/input_example/2020_wea.csv"


class UnitTests(unittest.TestCase):

    def test_read_wea_datas_smoke(self):
        """
        Smoke test to check the function runs.
        """
        file_dir = wea_data_dir
        clean_input_data.read_wea_datas(file_dir, 'wea')
        return

    def test_read_wea_datas_edge(self):
        """
        Edge test to test for .csv format
        """
        with self.assertRaises(TypeError):
            file_dir = ""
            clean_input_data.read_wea_datas(file_dir, 'wea')
        return

    def test_drop_dup_nun_smoke(self):
        """
        Smoke test to check the function runs.
        """
        wea_df = clean_input_data.read_wea_datas(wea_data_dir, 'wea')
        clean_input_data.drop_dup_nan(wea_df, 'date')
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
        file_dir = rad_data_dir
        clean_input_data.read_rad_datas(file_dir, 'rad')
        return

    def test_read_rad_datas_edge(self):
        """
        Edge test to test for .csv format.
        """
        with self.assertRaises(TypeError):
            file_dir = "../docs"
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
        df = pd.DataFrame()
        clean_input_data.cull_df(df)
        return

    # def test_cull_df_edge(self):
    #     """
    #     Edge test to check there is time stamp (pandas datetime datatype).
    #     """
    #     with self.assertRaises(V):

    #     return

    # def save_df_to_csv_smoke(self):
    #     """
    #     Smoke test to check file_dir exists.
    #     """
    #     with self.assertRaises(V):

    #     return
