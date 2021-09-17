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

    # print(db_conn.execute("select * from dump_names_temp;").all())
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
