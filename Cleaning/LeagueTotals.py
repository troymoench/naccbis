""" This script is used to calculate league totals for offense and pitching
and load into database """
# Standard library imports
import json
# Third party imports
import pandas as pd
# Local imports
import metrics
import utils


def select_bench_players(data):
    """ Select bench players. Used for determining replacement level
    :param data: A DataFrame of a team's player stats
    :returns: A DataFrame of players that weren't in the top 9 in PA
    """
    data = data.sort_values(by=["pa"], ascending=False)
    return data[9:]


def calc_replacement_level(totals, conn):
    """ Calculate Replacement Level metrics
    Replacement Level is defined as the average bench player
    :param
    :returns:
    """
    data = pd.read_sql_table("batters_overall", conn)
    data = data.loc[:, "fname":"fo"]
    # data = data[data["season"] == 2017]
    bench = data.groupby(["season", "team"]).apply(select_bench_players)
    bench = bench.reset_index(drop=True)

    bench_totals = bench.groupby("season").sum()
    bench_totals = metrics.basic_offensive_metrics(bench_totals)
    bench_totals = metrics.advanced_offensive_metrics(bench_totals, totals)

    bench_totals["off_pa"] = bench_totals["off"] / bench_totals["pa"]
    return bench_totals


if __name__ == "__main__":
    with open("../config.json") as f:
        config = json.load(f)
    utils.init_logging()

    conn = utils.connect_db(config)
    data = pd.read_sql_table("team_offense_overall", conn)

    cols = ['season', 'g', 'pa', 'ab', 'r', 'h', 'x2b', 'x3b', 'hr', 'rbi', 'bb',
            'so', 'sb', 'cs', 'hbp', 'sf', 'sh', 'tb', 'xbh', 'gdp', 'go', 'fo']

    totals = data[cols].groupby("season").sum()
    # print(totals)
    totals = metrics.basic_offensive_metrics(totals)

    totals["lg_r_pa"] = totals["r"] / totals["pa"]
    totals["bsr_bmult"] = metrics.bsr_bmult(totals)
    totals["bsr"] = metrics.bsr(totals, bmult=totals["bsr_bmult"])
    # print(totals)
    # print(metrics.linear_weights_incr(totals.loc[2018]))
    lw = totals.apply(metrics.linear_weights_incr, axis=1)
    # print(lw)
    totals = totals.join(lw)
    # print(totals)
    ww = metrics.woba_weights(totals, totals["obp"])
    # print(ww)
    totals = totals.join(ww)
    totals["woba"] = metrics.woba(totals, ww)
    totals["sbr"] = metrics.sbr(totals, lw)
    totals["lg_wsb"] = metrics.lg_wsb(totals, lw)
    totals["wsb"] = metrics.wsb(totals, totals["lg_wsb"])
    totals["wraa"] = metrics.wraa(totals, totals["woba"], totals["woba_scale"])
    totals["off"] = metrics.off(totals)
    totals["wrc"] = metrics.wrc(totals, totals["woba"], totals["woba_scale"], totals["lg_r_pa"])
    totals["wrc_p"] = metrics.wrc_p(totals, totals["lg_r_pa"])
    totals["off_p"] = metrics.off_p(totals, totals["lg_r_pa"])

    replacement_totals = calc_replacement_level(totals, conn)

    # Load replacement level totals in database
    utils.db_load_data(replacement_totals, "replacement_level", conn, if_exists="append", index=True)

    totals["rep_level"] = replacement_totals["off_pa"]
    totals["rar"] = metrics.rar(totals, totals["rep_level"])

    utils.db_load_data(totals, "league_offense_overall", conn, if_exists="append", index=True)

    # totals.to_csv("csv/league_offense_overall.csv")
    conn.close()
