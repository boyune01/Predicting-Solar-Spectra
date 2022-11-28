"""
This moudle is used for unit tests.
"""

import unittest
import os
import numpy as np
import pandas as pd

from code import read_wea_datas
from code import drop_dup_nan
from code import merge_df
from code import read_rad_datas

data_dir = "/mnt/c/Users/miche/Desktop/py_CSE583/Project_solar_spectrum/data"


class UnitTests(unittest.TestCase):
    """
    Define a class in which the tests will run.
    """

    # 1. Process Weather Data
    # 1.1 Smoke Test
    def test_smoke_wea(self):
        """
        Smoke test to make sure function runs for reading weather data.
        """
        wea_df = read_wea_datas(data_dir, 'wea')
        wea_df = drop_dup_nan(wea_df, 'date')

    def test_smoke_aod(self):
        """
        Smoke test to make sure function runs for reading aod data.
        """
        aod_df = read_wea_datas(data_dir, 'aod')
        aod_df = drop_dup_nan(aod_df, 'date')

    def test_smoke_prcp(self):
        """
        Smoke test to make sure function runs for 
        reading precipitable water data.
        """
        prcp_wtr_df = read_wea_datas(data_dir, 'precip')
        prcp_wtr_df["date"] = prcp_wtr_df["date"].dt.ceil(freq="30T")
        prcp_wtr_df = drop_dup_nan(prcp_wtr_df, 'date')

    def test_smoke_merge(self):
        """
        Smoke test to make sure function runs for merging data.
        """
        input_df = merge_df(wea_df, prcp_wtr_df, aod_df)

    # 1.2 Edge Test
    def test_edge_1(self):
        """
        Make sure the function throws a ValueError
        when the input file_dir is not .csv files.
        """
        with self.assertRaises(ValueError):
            # How to express it is not csv (data_dir)?
            # Each data wirte in one or sperate function?

    def test_edge_2(self):
        """
        Make sure the function throws a ValueError
        when the input file_dir do not have repeated name.
        """
        with self.assertRaises(ValueError):

    def test_edge_3(self):
        """
        Make sure the function throws a ValueError
        when the df files have only one column.
        """
        with self.assertRaises(ValueError):
            assert len(wea_df, prcp_wtr_df, aod_df) <= 1

    # 2. Process Radiation Data
    # 2.1 Smoke Test
    def test_smoke_rad(self):
        """
        Smoke test to make sure function runs for reading radiation data.
        """
        rad_df = read_rad_datas(data_dir, "rad")
