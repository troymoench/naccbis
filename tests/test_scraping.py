""" This module provides scraping unit tests """
# Standard library imports
# Third party imports
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import pytest
# Local imports
from naccbis.Scraping import (
    ScrapeFunctions,
    BaseScraper,
    GameLogScraper,
    IndividualOffenseScraper,
    IndividualPitchingScraper,
    TeamFieldingScraper,
    TeamOffenseScraper,
    TeamPitchingScraper,
)
from naccbis.scripts import scrape


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

    monkeypatch.setattr(ScrapeFunctions, "get_soup", mock_response)


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
        assert ScrapeFunctions.get_text(html_tag) == "Google"

    def test_get_href(self):
        soup = BeautifulSoup("<a href='https://www.google.com'> Google </a>", 'html.parser')
        html_tag = soup.a
        assert ScrapeFunctions.get_href(html_tag) == "https://www.google.com"

    def test_find_table(self, html_table):
        header_values = ["Col 1", "col 3"]
        soup = BeautifulSoup(html_table, "html.parser")
        assert ScrapeFunctions.find_table(soup, header_values) == [0]
        assert ScrapeFunctions.find_table(soup, ["Col 1", "Col 5"]) == []

    def test_scrape_table(self, html_table):
        df = pd.DataFrame({
            "Col 1": ["(1,1)", "(2,1)", "(3,1)", "(4,1)"],
            "Col 2": ["(1,2)", "(2,2)", "(3,2)", "(4,2)"],
            "Col 3": ["(1,3)", "(2,3)", "(3,3)", "(4,3)"],
            "Col 4": ["(1,4)", "(2,4)", "(3,4)", "(4,4)"]
        })
        soup = BeautifulSoup(html_table, "html.parser")
        assert df.equals(ScrapeFunctions.scrape_table(soup, 1))
        with pytest.raises(IndexError):
            ScrapeFunctions.scrape_table(soup, 2)

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
        assert ScrapeFunctions.get_team_list(self.BASE_URL, year, self.TEAM_IDS) == expected

    def test_skip_team(self):
        html = """
        <tr class="totals">
        <td colspan="5">
              No players meet the minimum
            </td>
        </tr>
        """
        soup = BeautifulSoup(html, 'html.parser')
        assert ScrapeFunctions.skip_team(soup)


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


class TestIndividualOffenseScraper():
    def test_info(self):
        scraper = IndividualOffenseScraper("2018-19", "overall", "csv")
        scraper.info()

    def test_clean(self):
        scraper = IndividualOffenseScraper("2018-19", "overall", "csv")
        raw_cols = [
            'No.', 'Name', 'Yr', 'Pos', 'g', 'ab', 'r', 'h', '2b', '3b', 'hr', 'rbi',
            'bb', 'k', 'sb', 'cs', 'avg', 'obp', 'slg', 'hbp', 'sf', 'sh', 'tb', 'xbh',
            'hdp', 'go', 'fo', 'go/fo', 'pa'
        ]
        raw_df = pd.DataFrame([
            ('3', 'Jonathan  Hodo', 'So.', 'INF', '41', '161', '23', '48', '7', '1', '-',
                '26', '12', '24', '11', '3', '.298', '.370', '.354', '7', '1', '-',
                '57', '8', '3', '40', '45', '0.89', '181'),
            ('9', 'Jack  Surin', 'Fr.', '', '41', '150', '18', '39', '10', '-', '-',
                '22', '8', '16', '7', '-', '.260', '.307', '.327', '3', '2', '2', '49',
                '10', '2', '39', '55', '0.71', '165')
        ], columns=raw_cols)
        expected_cols = [
            'no', 'name', 'team', 'season', 'yr', 'pos', 'g', 'pa', 'ab', 'r', 'h',
            'x2b', 'x3b', 'hr', 'rbi', 'bb', 'so', 'sb', 'cs', 'avg', 'obp', 'slg',
            'hbp', 'sf', 'sh', 'tb', 'xbh', 'gdp', 'go', 'fo', 'go_fo'
        ]
        expected = pd.DataFrame([
            ('3', 'Jonathan  Hodo', 'BEN', '2019', 'So', 'INF', '41', '181', '161', '23', '48',
                '7', '1', '0', '26', '12', '24', '11', '3', '.298', '.370', '.354',
                '7', '1', '0', '57', '8', '3', '40', '45', '0.89'),
            ('9', 'Jack  Surin', 'BEN', '2019', 'Fr', np.nan, '41', '165', '150', '18', '39',
                '10', '0', '0', '22', '8', '16', '7', '0', '.260', '.307', '.327',
                '3', '2', '2', '49', '10', '2', '39', '55', '0.71')
        ], columns=expected_cols)
        assert expected.equals(scraper._clean(raw_df, "BEN"))


class TestIndividualPitchingScraper():
    def test_info(self):
        scraper = IndividualPitchingScraper("2018-19", "overall", "csv")
        scraper.info()

    def test_clean_overall(self):
        scraper = IndividualPitchingScraper("2018-19", "overall", "csv")
        raw_cols = [
            'No.', 'Name', 'ERA', 'W', 'L', 'APP', 'GS', 'CG', 'SHO', 'SV', 'IP',
            'H', 'R', 'ER', 'BB', 'SO', '2B', '3B', 'HR', 'AB', 'B/AVG', 'WP', 'HBP',
            'BK', 'SFA', 'SHA', 'Yr', 'Pos', 'app', 'gs', 'w', 'l', 'sv', 'cg', 'ip',
            'h', 'r', 'er', 'bb', 'k', 'k/9', 'hr', 'era'
        ]
        raw_df = pd.DataFrame([
            ('31', 'Nicholas Mathey', '2.28', '2', '0', '20', '0', '-', '-', '12',
                '43.1', '31', '15', '11', '8', '47', '2', '-', '2', '153', '.203',
                '5', '1', '-', '1', '2', 'Sr.', 'OF/P', '20', '0', '2', '0', '12', '-',
                '43.1', '31', '15', '11', '8', '47', '9.76', '2', '2.28'),
            ('32', 'Michael Fidler', '2.53', '1', '1', '13', '0', '-', '-', '4',
                '21.1', '16', '6', '6', '9', '17', '4', '-', '1', '72', '.222', '5',
                '7', '-', '2', '2', 'Sr.', 'P/IF', '13', '0', '1', '1', '4', '-',
                '21.1', '16', '6', '6', '9', '17', '7.17', '1', '2.53')
        ], columns=raw_cols)
        expected_cols = [
            'no', 'name', 'team', 'season', 'yr', 'pos', 'g', 'gs', 'w', 'l', 'sv',
            'cg', 'sho', 'ip', 'h', 'r', 'er', 'bb', 'so', 'era', 'x2b', 'x3b', 'hr',
            'ab', 'avg', 'wp', 'hbp', 'bk', 'sf', 'sh', 'so_9'
        ]
        expected = pd.DataFrame([
            ('31', 'Nicholas Mathey', 'AUR', '2019', 'Sr', 'OF/P', '20', '0', '2',
                '0', '12', '0', '0', '43.1', '31', '15', '11', '8', '47', '2.28',
                '2', '0', '2', '153', '.203', '5', '1', '0', '1', '2', '9.76'),
            ('32', 'Michael Fidler', 'AUR', '2019', 'Sr', 'P/IF', '13', '0', '1',
                '1', '4', '0', '0', '21.1', '16', '6', '6', '9', '17', '2.53',
                '4', '0', '1', '72', '.222', '5', '7', '0', '2', '2', '7.17')
        ], columns=expected_cols)
        assert expected.equals(scraper._clean(raw_df, "AUR"))


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
