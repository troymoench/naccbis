""" This module provides data cleaning unit tests """

import unittest
import CleanFunctions as cf


class TestCleanFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_id(self):
        self.assertEqual(cf.create_id("Curtis", "Engelbrecht"), "engelcu01")

    def test_add_n(self):
        self.assertEqual(cf.add_n("engelcu01", 2), "engelcu03")

    # def test_normalize_names(self):
    #     pass
    #
    # def test_apply_corrections(self):
    #     pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
