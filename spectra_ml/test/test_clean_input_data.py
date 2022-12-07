"""
Test function
"""
import os
import unittest
from code import clean_input_data

data_dir = "/Volumes/GoogleDrive/My Drive/COURSES/22 AU/CSE_583/final_prj/data/raw/"


class UnitTests(unittest.TestCase):

    def test_read_wea_datas_smoke(self):
        """
        Smoke test to check the function runs.
        """
        file_dir = data_dir
        clean_input_data.read_wea_datas(file_dir, 'wea')
        return

    def test_read_wea_datas_edge(self):
        """
        Edge test to test for .csv format
        """
        with self.assertRaises(TypeError):
            for file in files:  # Q: WE WANT TO CHECK 'FILES' WHICH IS A VALUE INSIDE 'READ_WEA_DATAS' FUNCTION. HOW DO WE ACCESS A VALUE INSIDE A FUNCTION?
                # Split the extension from the path and normalise it to lowercase.
                ext = os.path.splitext(file)[-1].lower()
                if ext == ".csv":
                    pass
            file_dir = "...."
            clean_input_data.read_wea_datas(file_dir, 'wea')
        return

    def test_drop_dup_nun_smoke(self):
        """
        Smoke test to check the function runs.
        """
        wea_df = clean_input_data.read_wea_datas(data_dir, 'wea')
        clean_input_data.drop_dup_nan(wea_df, 'date')
        return

    def test_merge_df_edge(self):
        """
        Check there are multiple dataframes.
        """
        with self.assertRaises(TypeError):
            clean_input_data.merge_df(wea_df)  # Only one dataframe
        return

    def test_read_rad_datas_smoke(self):
        """
        Smoke test to check the function runs.
        """
        file_dir = data_dir
        clean_input_data.read_rad_datas(file_dir, 'rad')
        return

    def test_read_rad_datas_edge(self):
        """
        Edge test to test for .csv format
        """
        with self.assertRaises(TypeError):
            for file in files:  # Q: WE WANT TO CHECK 'FILES' WHICH IS A VALUE INSIDE 'READ_WEA_DATAS' FUNCTION. HOW DO WE ACCESS A VALUE INSIDE A FUNCTION?
                # Split the extension from the path and normalise it to lowercase.
                ext = os.path.splitext(file)[-1].lower()
                if ext == ".csv":
                    pass
            file_dir = "...."
            clean_input_data.read_rad_datas(file_dir, 'rad')
        return

    def test_interpolation_1nm_edge1(self):
        """
        Edge test to check there is only wavelength data.
        """

    def test_interpolation_1nm_edge2(self):
        """
        Edge test to check the number of column.
        """

    def test_cull_df_smoke(self):
        """
        Smoke test to check there are 2 dataframes.
        """

    def test_cull_df_edge(self):
        """
        Edge test to check there is time stamp (pandas datetime datatype).
        """

    def save_df_to_csv_smoke(self):
        """
        Smoke test to check file_dir exists.
        """
