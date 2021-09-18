import pandas as pd
import pytest
from naccbis.scripts import DumpNames


@pytest.fixture(scope="module")
def create_temp_table(db_conn):
    DumpNames.load_temp_table(db_conn, pd.DataFrame())
    yield
    db_conn.execute("DROP TABLE dump_names_temp;")


def test_nickname_analysis(db_conn, create_temp_table):
    db_conn.execute(
        "INSERT INTO dump_names_temp (lname, fname, team, season, pos) VALUES "
        "('Bergstrom', 'Michael', 'MSOE', 2010, 'P'),"
        "('Bergstrom', 'Mike', 'MSOE', 2011, ''),"
        "('Bergstrom', 'Michael', 'MSOE', 2012, 'P'),"
        "('Bergstrom', 'Mike', 'MSOE', 2013, 'P'),"
        "('Buckley', 'Mike', 'DOM', 2017, 'C'),"
        "('Buckley', 'Mike', 'DOM', 2018, 'C');"
    )
    db_conn.execute(
        "INSERT INTO nicknames (name, nickname) VALUES "
        "('Michael', 'Micah'),"
        "('Michael', 'Mick'),"
        "('Michael', 'Micky'),"
        "('Michael', 'Mike');"
    )

    expected = pd.DataFrame(
        [
            ("Bergstrom", "Michael", "MSOE", 2010, "Mike", "MSOE", 2013),
            ("Bergstrom", "Michael", "MSOE", 2010, "Mike", "MSOE", 2011),
            ("Bergstrom", "Michael", "MSOE", 2012, "Mike", "MSOE", 2013),
            ("Bergstrom", "Michael", "MSOE", 2012, "Mike", "MSOE", 2011),
        ],
        columns=["lname", "fname1", "team1", "season1", "fname2", "team2", "season2"],
    )
    assert expected.equals(DumpNames.nickname_analysis(db_conn))


def test_levenshtein_analysis_last_name_1_first_name_0(db_conn, create_temp_table):
    db_conn.execute(
        "INSERT INTO dump_names_temp (lname, fname, team, season, pos) VALUES "
        "('Ikedia-Flynn', 'Kanoa','DOM', 2017, 'P'),"
        "('Ikeda-Flynn', 'Kanoa','DOM', 2018, 'P'),"
        "('Ikeda-Flynn', 'Kanoa','DOM', 2019, 'P'),"
        "('Baitinger', 'Sawyer', 'MAR', 2014, 'RHP'),"
        "('Batinger', 'Sawyer', 'MAR', 2015, 'RHP');"
    )

    expected = pd.DataFrame(
        [
            (
                "Baitinger",
                "Sawyer",
                "MAR",
                2014,
                "RHP",
                "Batinger",
                "Sawyer",
                "MAR",
                2015,
                "RHP",
            ),
            (
                "Batinger",
                "Sawyer",
                "MAR",
                2015,
                "RHP",
                "Baitinger",
                "Sawyer",
                "MAR",
                2014,
                "RHP",
            ),
            (
                "Ikeda-Flynn",
                "Kanoa",
                "DOM",
                2018,
                "P",
                "Ikedia-Flynn",
                "Kanoa",
                "DOM",
                2017,
                "P",
            ),
            (
                "Ikeda-Flynn",
                "Kanoa",
                "DOM",
                2019,
                "P",
                "Ikedia-Flynn",
                "Kanoa",
                "DOM",
                2017,
                "P",
            ),
            (
                "Ikedia-Flynn",
                "Kanoa",
                "DOM",
                2017,
                "P",
                "Ikeda-Flynn",
                "Kanoa",
                "DOM",
                2018,
                "P",
            ),
            (
                "Ikedia-Flynn",
                "Kanoa",
                "DOM",
                2017,
                "P",
                "Ikeda-Flynn",
                "Kanoa",
                "DOM",
                2019,
                "P",
            ),
        ],
        columns=[
            "lname1",
            "fname1",
            "team1",
            "season1",
            "pos1",
            "lname2",
            "fname2",
            "team2",
            "season2",
            "pos2",
        ],
    )

    assert expected.equals(
        DumpNames.levenshtein_analysis(db_conn, lev_first=0, lev_last=1)
    )


def test_levenshtein_analysis_last_name_0_first_name_1(db_conn, create_temp_table):
    db_conn.execute(
        "INSERT INTO dump_names_temp (lname, fname, team, season, pos) VALUES "
        "('Hart', 'Collin', 'AUR', 2014, 'P'),"
        "('Hart', 'Colin', 'AUR', 2015, 'P'),"
        "('Stirbis', 'Chayancze', 'BEN', 2016, ''),"
        "('Stirbis', 'Chayance', 'BEN', 2017, '');"
    )

    expected = pd.DataFrame(
        [
            ("Hart", "Colin", "AUR", 2015, "P", "Hart", "Collin", "AUR", 2014, "P"),
            ("Hart", "Collin", "AUR", 2014, "P", "Hart", "Colin", "AUR", 2015, "P"),
            (
                "Stirbis",
                "Chayance",
                "BEN",
                2017,
                "",
                "Stirbis",
                "Chayancze",
                "BEN",
                2016,
                "",
            ),
            (
                "Stirbis",
                "Chayancze",
                "BEN",
                2016,
                "",
                "Stirbis",
                "Chayance",
                "BEN",
                2017,
                "",
            ),
        ],
        columns=[
            "lname1",
            "fname1",
            "team1",
            "season1",
            "pos1",
            "lname2",
            "fname2",
            "team2",
            "season2",
            "pos2",
        ],
    )

    assert expected.equals(
        DumpNames.levenshtein_analysis(db_conn, lev_first=1, lev_last=0)
    )
