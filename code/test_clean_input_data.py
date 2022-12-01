"""
Test function
"""
import os
import unittest
from code import clean_input_data

data_dir = "/Volumes/GoogleDrive/My Drive/COURSES/22 AU/CSE_583/final_prj/data/raw/"

class UnitTests(unittest.TestCase):
    def test_read_wea_datas(self):
        """
        Edge test to test for .csv format
        """
        with self.assertRaises(ValueError):
            for file in files:  # Q: WE WANT TO CHECK 'FILES' WHICH IS A VALUE INSIDE 'READ_WEA_DATAS' FUNCTION. HOW DO WE ACCESS A VALUE INSIDE A FUNCTION?
                # Split the extension from the path and normalise it to lowercase.
                ext = os.path.splitext(file)[-1].lower()
                if ext == ".csv":
                    pass
        
        return

    def test_
