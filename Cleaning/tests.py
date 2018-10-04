""" This module provides data cleaning unit tests """

import unittest
import CleanFunctions as cf
import pandas as pd


class TestCleanFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_id(self):
        self.assertEqual(cf.create_id("Curtis", "Engelbrecht"), "engelcu01")

    def test_add_n(self):
        self.assertEqual(cf.add_n("engelcu01", 2), "engelcu03")

    def test_normalize_names(self):
        df1 = pd.DataFrame({"name": ["Jeffrey  Mayes", "D.J.  Dillon", "Quinlan Milne Rojek"],
                            "team": ["AUR", "BEN", "DOM"],
                            "season": [2017, 2017, 2016]}, columns=["name", "team", "season"])
        df2 = pd.DataFrame(df1)
        df2["fname"] = ["Jeffrey", "DJ", "Quinlan"]
        df2["lname"] = ["Mayes", "Dillon", "Milne Rojek"]
        self.assertTrue(cf.normalize_names(df1).equals(df2))

    # def test_apply_corrections(self):
    #     pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
