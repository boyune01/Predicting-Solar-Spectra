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
    
    def test_read_wea_datas_edge1(self):
        """
        Edge test to test for .csv format
        """
        with self.assertRaises(TypeError):
            file_dir = "...."
            clean_input_data.read_wea_datas(file_dir, 'wea')
        
        return

    # def 
