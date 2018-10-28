""" This module provides scraping unit tests """
# Standard library imports
import unittest
# Third party imports
from bs4 import BeautifulSoup
import pandas as pd
# Local imports
import ScrapeFunctions as sf


class TestScrapeFunctions(unittest.TestCase):

    """ Unit tests for scraping functions """

    def setUp(self):
        self.html = """<div class='container'>
                <table>
                <tr>
                    <th>Col 1</th>
                    <th>Col 2</th>
                    <th>Col 3</th>
                    <th>Col 4</th>
                </tr>
                <tr>
                    <td>(1,1)</td>
                    <td>(1,2)</td>
                    <td>(1,3)</td>
                    <td>(1,4)</td>
                </tr>
                <tr>
                    <td>(2,1)</td>
                    <td>(2,2)</td>
                    <td>(2,3)</td>
                    <td>(2,4)</td>
                </tr>
                <tr>
                    <td>(3,1)</td>
                    <td>(3,2)</td>
                    <td>(3,3)</td>
                    <td>(3,4)</td>
                </tr>
                <tr>
                    <td>(4,1)</td>
                    <td>(4,2)</td>
                    <td>(4,3)</td>
                    <td>(4,4)</td>
                </tr>
                <tbody></tbody>
                </table>
        </div>"""
        self.df = pd.DataFrame({"Col 1": ["(1,1)", "(2,1)", "(3,1)", "(4,1)"],
                                "Col 2": ["(1,2)", "(2,2)", "(3,2)", "(4,2)"],
                                "Col 3": ["(1,3)", "(2,3)", "(3,3)", "(4,3)"],
                                "Col 4": ["(1,4)", "(2,4)", "(3,4)", "(4,4)"]})

    def test_get_text(self):
        soup = BeautifulSoup("<a href='https://www.google.com'> Google </a>", 'html.parser')
        html_tag = soup.a
        self.assertEqual(sf.get_text(html_tag), "Google")

    def test_get_href(self):
        soup = BeautifulSoup("<a href='https://www.google.com'> Google </a>", 'html.parser')
        html_tag = soup.a
        self.assertEqual(sf.get_href(html_tag), "https://www.google.com")

    def test_find_table(self):
        header_values = ["Col 1", "col 3"]
        soup = BeautifulSoup(self.html, "html.parser")
        self.assertEqual(sf.find_table(soup, header_values), [0])
        self.assertEqual(sf.find_table(soup, ["Col 1", "Col 5"]), [])

    def test_scrape_table(self):
        soup = BeautifulSoup(self.html, "html.parser")
        self.assertTrue(self.df.equals(sf.scrape_table(soup, 1)))
        with self.assertRaises(IndexError):
            sf.scrape_table(soup, 2)

    def test_year_to_season(self):
        year = "2016-17"
        self.assertEqual(sf.year_to_season(year), 2017)

    def test_season_to_year(self):
        season = 2017
        self.assertEqual(sf.season_to_year(season), "2016-17")

    def test_strip_dots(self):
        name = "Jeffrey Mayes......."
        self.assertEqual(sf.strip_dots(name), "Jeffrey Mayes")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
