""" This script is used to clean game log data and load into the database """
# Standard library imports
import argparse
import datetime
import json
import re
import sys
# Third party imports
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
# Local imports
import CleanFunctions as cf
import utils


def extract_runs(score):
    """ Extract the runs scored and runs against from the score
    :param score: The score
    :returns: A list where first element is runs scored and
     second element is runs against. Format: [rs, ra]
    """
    split_score = score.split(',')
    result = split_score[0].strip()
    run_list = split_score[1].split('-')
    run_list = list(map(lambda x: int(x.strip()), run_list))

    if result == 'W':
        run_list.sort(reverse=True)
    else:
        run_list.sort()
    return run_list


def extract_result(score):
    """ Extract the result (W/L) from the score
    :param score: The score
    :returns: The result (W/L)
    """
    return score.split(',')[0].strip()


def extract_home(opponent):
    """ Extract home/away from the opponent
    :param opponent: The opponent
    :returns: True for home, False for away
    """
    opponent = opponent.strip()
    if re.match(r"\b[Aa][Tt]\b", opponent):
        home = False
    else:
        home = True
    return home


def extract_opponent(opponent):
    """ Extract the team name from the raw opponent
    :param opponent: The opponent
    :returns: The team name of the opponent
    """
    opponent = opponent.strip()
    return re.sub(r"\b[Aa][Tt]\b|\b[Vv][Ss][.]*", "", opponent).strip()


def extract_conference(opponent, season, teams):
    # Maranatha is non-conference after 2013
    if opponent == "Maranatha" and season > 2013:
        return False

    matched = False
    for team in teams:
        if re.search(team, opponent):
            matched = True
    return matched


def extract_date(date_str, season):
    date_str = "{} {}".format(date_str, season)
    return datetime.datetime.strptime(date_str, "%b %d %Y")


def clean(data):
    data = data.copy()
    data["result"] = data["score"].apply(extract_result)
    # runs scored, runs against

    data["inter"] = data["score"].apply(extract_runs)  # intermediate column
    data["rs"] = [x[0] for x in data["inter"]]
    data["ra"] = [x[1] for x in data["inter"]]

    data.drop(columns=["inter"], inplace=True)

    # home/away

    data["home"] = data["opponent"].apply(extract_home)

    # conference/non-conference

    conf = ["Aurora", "Benedictine", "Concordia Chicago", "Concordia Wisconsin", "Dominican",
            "Edgewood", "Lakeland", "MSOE", "Marian", "Maranatha", "Rockford", "Wisconsin Lutheran"]

    data["conference"] = list(map(lambda x, y: extract_conference(x, y, conf), data["opponent"], data["season"]))
    data["opponent"] = data["opponent"].apply(extract_opponent)
    data.rename(columns={"name": "team"}, inplace=True)
    data.drop(columns=["score"], inplace=True)

    data["date"] = list(map(lambda x, y: extract_date(x, y), data["date"], data["season"]))
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract, Transform, Load Game Log data")
    parser.add_argument("--load", action="store_true",
                        help="Load data into database")
    args = parser.parse_args()

    with open('../config.json') as f:
        config = json.load(f)

    CSV_DIR = "csv/"

    conn = utils.connect_db(config)

    data = pd.read_sql_table("raw_game_log_hitting", conn)

    data = data[["game_num", "date", "season", "name", "opponent", "score"]]
    # print(data)
    data = clean(data)
    if args.load:
        print("Loading data into database")
        try:
            data.to_sql("game_log", conn, if_exists="append", index=False)
        except SQLAlchemyError as e:
            print("Failed to load data into database")
            print(e)
            conn.close()
            sys.exit(1)
        print("Loaded successfully")
    else:
        print("Dumping to csv")
        data.to_csv(CSV_DIR + "game_log.csv", index=False)
    conn.close()