""" This module provides scraping unit tests """
# Standard library imports
# Third party imports
from bs4 import BeautifulSoup
import pandas as pd
import pytest
# Local imports
import naccbis.Scraping.ScrapeFunctions as sf
from naccbis.Scraping import (
    BaseScraper,
    GameLogScraper,
    IndividualOffenseScraper,
    IndividualPitchingScraper,
    TeamFieldingScraper,
    TeamOffenseScraper,
    TeamPitchingScraper,
)
import naccbis.scripts.scrape as scrape


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


@pytest.fixture
def mock_get_soup(monkeypatch):
    def mock_response(url):
        html = """
        <div class="cols">
        <div class="col">
        <h3>Sortable Team Stats</h3>
        <ul>
        <li><a aria-label="team stats - runs" href="teams?sort=r">Runs</a></li>
        <li><a aria-label="team stats - home runs" href="teams?sort=hr">Home Runs</a></li>
        <li><a aria-label="team stats - batting average" href="teams?sort=avg">Batting Average</a></li>
        <li><a aria-label="team stats - more" href="teams">More Stats</a></li>
        </ul>
        </div>
        <div class="col">
        <h3>Player Stats by Team</h3>
        <ul>
        <li><a aria-label="players stats - Aurora" href="teams/aurora?view=lineup">Aurora</a></li>
        <li><a aria-label="players stats - Benedictine" href="teams/benedictineil?view=lineup">Benedictine</a></li>
        <li><a aria-label="players stats - Concordia Chicago" href="teams/concordiaill?view=lineup">Concordia Chicago</a></li>
        <li><a aria-label="players stats - Concordia Wisconsin" href="teams/concordiawis?view=lineup">Concordia Wisconsin</a></li>
        <li><a aria-label="players stats - Dominican" href="teams/dominicanill?view=lineup">Dominican</a></li>
        <li><a aria-label="players stats - Edgewood" href="teams/edgewood?view=lineup">Edgewood</a></li>
        <li><a aria-label="players stats - Lakeland" href="teams/lakeland?view=lineup">Lakeland</a></li>
        <li><a aria-label="players stats - MSOE" href="teams/msoe?view=lineup">MSOE</a></li>
        <li><a aria-label="players stats - Marian" href="teams/marianwis?view=lineup">Marian</a></li>
        <li><a aria-label="players stats - Rockford" href="teams/rockford?view=lineup">Rockford</a></li>
        <li><a aria-label="players stats - Wisconsin Lutheran" href="teams/wislutheran?view=lineup">Wisconsin Lutheran</a></li>
        </ul>
        </div>
        </div>
        """
        return BeautifulSoup(html, "html.parser")

    monkeypatch.setattr(sf, "get_soup", mock_response)


class TestScrapeFunctions():
    BASE_URL = 'https://naccsports.org/sports/bsb/'
    TEAM_IDS = {
        'Aurora': 'AUR',
        'Benedictine': 'BEN',
        'Concordia Chicago': 'CUC',
        'Concordia Wisconsin': 'CUW',
        'Dominican': 'DOM',
        'Edgewood': 'EDG',
        'Illinois Tech': 'ILLT',
        'Lakeland': 'LAK',
        'MSOE': 'MSOE',
        'Marian': 'MAR',
        'Maranatha': 'MARN',
        'Rockford': 'ROCK',
        'Wisconsin Lutheran': 'WLC'
    }

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

    def test_get_team_list(self, mock_get_soup):
        year = '2017-18'
        expected = [
            {'team': 'Aurora', 'id': 'AUR', 'url': 'teams/aurora?view=lineup'},
            {'team': 'Benedictine', 'id': 'BEN', 'url': 'teams/benedictineil?view=lineup'},
            {'team': 'Concordia Chicago', 'id': 'CUC', 'url': 'teams/concordiaill?view=lineup'},
            {'team': 'Concordia Wisconsin', 'id': 'CUW', 'url': 'teams/concordiawis?view=lineup'},
            {'team': 'Dominican', 'id': 'DOM', 'url': 'teams/dominicanill?view=lineup'},
            {'team': 'Edgewood', 'id': 'EDG', 'url': 'teams/edgewood?view=lineup'},
            {'team': 'Lakeland', 'id': 'LAK', 'url': 'teams/lakeland?view=lineup'},
            {'team': 'MSOE', 'id': 'MSOE', 'url': 'teams/msoe?view=lineup'},
            {'team': 'Marian', 'id': 'MAR', 'url': 'teams/marianwis?view=lineup'},
            {'team': 'Rockford', 'id': 'ROCK', 'url': 'teams/rockford?view=lineup'},
            {'team': 'Wisconsin Lutheran', 'id': 'WLC', 'url': 'teams/wislutheran?view=lineup'},
        ]
        assert sf.get_team_list(self.BASE_URL, year, self.TEAM_IDS) == expected

    def test_skip_team(self):
        html = """
        <tr class="totals">
        <td colspan="5">
              No players meet the minimum
            </td>
        </tr>
        """
        soup = BeautifulSoup(html, 'html.parser')
        assert sf.skip_team(soup)


def test_cant_instantiate_base_scraper():
    with pytest.raises(TypeError):
        BaseScraper("2018", "overall", "csv")


def test_init_scrapers():
    scrapers = [
        GameLogScraper("2018", "overall", "csv"),
        IndividualOffenseScraper("2018", "overall", "csv"),
        IndividualPitchingScraper("2018", "overall", "csv"),
        TeamFieldingScraper("2018", "overall", "csv"),
        TeamOffenseScraper("2018", "overall", "csv"),
        TeamPitchingScraper("2018", "overall", "csv"),
    ]
    for scraper in scrapers:
        assert isinstance(scraper, BaseScraper)


def test_parse_args_final_defaults():
    args = scrape.parse_args(['final', '2019'])
    assert callable(args.func)
    assert args.year == [2019]
    assert args.stat == range(1, 7)
    assert args.split == 'all'
    assert args.output == 'csv'
    assert not args.verbose


def test_parse_args_final_stat():
    args = scrape.parse_args(['final', '2019', '-S', '1', '2'])
    assert callable(args.func)
    assert args.year == [2019]
    assert args.stat == [1, 2]
    assert args.split == 'all'
    assert args.output == 'csv'
    assert not args.verbose


def test_parse_args_inseason_defaults():
    args = scrape.parse_args(['inseason'])
    assert callable(args.func)
    assert args.stat == range(1, 7)
    assert args.split == 'all'
    assert args.output == 'csv'
    assert not args.verbose


def test_parse_args_inseason_stat():
    args = scrape.parse_args(['inseason', '-S', '1', '2'])
    assert callable(args.func)
    assert args.stat == [1, 2]
    assert args.split == 'all'
    assert args.output == 'csv'
    assert not args.verbose
