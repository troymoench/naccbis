""" This module provides scraping unit tests """
# Standard library imports
# Third party imports
from bs4 import BeautifulSoup
import pandas as pd
import pytest
# Local imports
import naccbis.Scraping.ScrapeFunctions as sf


@pytest.fixture
def html_table():
    return """<div class='container'>
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


class TestScrapeFunctions():

    def test_get_text(self):
        soup = BeautifulSoup("<a href='https://www.google.com'> Google </a>", 'html.parser')
        html_tag = soup.a
        assert sf.get_text(html_tag) == "Google"

    def test_get_href(self):
        soup = BeautifulSoup("<a href='https://www.google.com'> Google </a>", 'html.parser')
        html_tag = soup.a
        assert sf.get_href(html_tag) == "https://www.google.com"

    def test_find_table(self, html_table):
        header_values = ["Col 1", "col 3"]
        soup = BeautifulSoup(html_table, "html.parser")
        assert sf.find_table(soup, header_values) == [0]
        assert sf.find_table(soup, ["Col 1", "Col 5"]) == []

    def test_scrape_table(self, html_table):
        df = pd.DataFrame({
            "Col 1": ["(1,1)", "(2,1)", "(3,1)", "(4,1)"],
            "Col 2": ["(1,2)", "(2,2)", "(3,2)", "(4,2)"],
            "Col 3": ["(1,3)", "(2,3)", "(3,3)", "(4,3)"],
            "Col 4": ["(1,4)", "(2,4)", "(3,4)", "(4,4)"]
        })
        soup = BeautifulSoup(html_table, "html.parser")
        assert df.equals(sf.scrape_table(soup, 1))
        with pytest.raises(IndexError):
            sf.scrape_table(soup, 2)

    def test_strip_dots(self):
        name = "Jeffrey Mayes......."
        assert sf.strip_dots(name) == "Jeffrey Mayes"
