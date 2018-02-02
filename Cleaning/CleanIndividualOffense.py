import pandas as pd
from sqlalchemy import create_engine
import CleanFunctions

SPLIT = "overall"
OUTPUT = "csv"

engine = create_engine('postgresql+psycopg2://troy:baseballisfun@172.16.21.93:5432/naccbisdb')
conn = engine.connect()

data = pd.read_sql_table("raw_batters_{}".format(SPLIT), conn)
conn.close()


# ***********************************
# ****** NAME NORMALIZATION *********
# ***********************************

# split each name into first name and last name
data["fname"] = [x.split("  ")[0] for x in data["name"]]
data["lname"] = [x.split("  ")[1] for x in data["name"]]

# remove periods from first name
data["fname"] = [x.replace(".", "") for x in data["fname"]]

# output names for exploration
# 1. Inconsistent spellings
# 2. Name changes
# 3. Transfers (for IDs)
# 4. Same name, different people (for IDs)
# Map corrected player-seasons to uncorrected player-seasons (dictionary? DataFrame? JSON?)


# data = data[["lname", "fname", "team", "season", "yr", "pos"]]
data = data.sort_values(by=["lname", "fname", "season"])
# data.to_csv("names.csv", index=False)

# print(data.head())

# *****************************
# ***** Name Corrections ******
# *****************************

# TODO: Make this a function
corrections = pd.read_csv("name_corrections.csv")
# print(corrections)

for i in range(len(corrections)):
    row = corrections.iloc[i]
    # print(row)
    need_update = pd.Series((data["fname"] == row["uc_fname"]) &
                            (data["lname"] == row["uc_lname"]) &
                            (data["team"] == row["uc_team"]) &
                            (data["season"] == row["uc_season"]))
    if need_update.sum() > 1:
        print("Must update one row at a time!")
        exit(1)
    if need_update.sum() == 0:
        print("No update")
        continue
    # print("Row to be updated:")
    # print(data[need_update], "\n")

    # update first name and last name with corrections
    data.loc[need_update, 'fname'] = row["c_fname"]
    data.loc[need_update, 'lname'] = row["c_lname"]

# data.to_csv("data.csv", index=False)


# iterate through groups of names to find same names but different teams
# manually verify transfers and different people using team rosters


# *******************************
# ****** Assign Player ID's *****
# *******************************

# data = pd.read_csv("data.csv")

data = CleanFunctions.set_ids(data, file="same_names.json", verbose=True)

# *******************************
# ***** Export Cleaned Data *****
# *******************************

# TODO: export options: csv, db

table_name = "clean_batters_{}".format(SPLIT)
data.drop(columns=["fname", "lname"], inplace=True)

finalColNames = data.axes[1].tolist()
finalColNames.remove("id")
finalColNames.insert(0, "id")
data = data[finalColNames]

data.to_csv("csv/{}.csv".format(table_name), index=False)
