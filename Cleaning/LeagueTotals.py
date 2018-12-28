""" This script is used to calculate league totals for offense and pitching
and load into database """
# Standard library imports
import json
# Third party imports
import pandas as pd
# Local imports
import metrics
import utils


class LeagueOffenseETL:
    """ ETL class for league offense """
    VALID_SPLITS = ["overall", "conference"]

    def __init__(self, split, conn):
        if split not in self.VALID_SPLITS:
            raise ValueError("Invalid split: {}".format(split))
        self.split = split
        self.conn = conn

    def extract(self):
        self.team_data = pd.read_sql_table("team_offense_{}".format(self.split), self.conn)
        self.batters = pd.read_sql_table("batters_{}".format(self.split), self.conn)

    def transform(self):
        cols = ['season', 'g', 'pa', 'ab', 'r', 'h', 'x2b', 'x3b', 'hr', 'rbi', 'bb',
                'so', 'sb', 'cs', 'hbp', 'sf', 'sh', 'tb', 'xbh', 'gdp', 'go', 'fo']

        totals = self.team_data[cols].groupby("season").sum()
        totals = metrics.basic_offensive_metrics(totals)

        totals["lg_r_pa"] = totals["r"] / totals["pa"]
        totals["bsr_bmult"] = metrics.bsr_bmult(totals)
        totals["bsr"] = metrics.bsr(totals, bmult=totals["bsr_bmult"])
        lw = totals.apply(metrics.linear_weights_incr, axis=1)
        totals = totals.join(lw)
        ww = metrics.woba_weights(totals, totals["obp"])
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

        replacement_totals = self.calc_replacement_level(totals)
        totals["rep_level"] = replacement_totals["off_pa"]
        totals["rar"] = metrics.rar(totals, totals["rep_level"])

        self.replacement_totals = replacement_totals
        self.totals = totals

    def load(self):
        utils.db_load_data(self.replacement_totals, "replacement_level_{}".format(self.split),
                           self.conn, if_exists="append", index=True)
        utils.db_load_data(self.totals, "league_offense_{}".format(self.split),
                           self.conn, if_exists="append", index=True)

    def run(self):
        self.extract()
        self.transform()
        self.load()

    @staticmethod
    def select_bench_players(data):
        """ Select bench players. Used for determining replacement level
        :param data: A DataFrame of a team's player stats
        :returns: A DataFrame of players that weren't in the top 9 in PA
        """
        data = data.sort_values(by=["pa"], ascending=False)
        return data[9:]

    def calc_replacement_level(self, totals):
        """ Calculate Replacement Level metrics
        Replacement Level is defined as the average bench player
        :param totals: A DataFrame of league totals
        :returns: A DataFrame of replacement level totals
        """
        temp = self.batters.loc[:, "fname":"fo"]
        bench = temp.groupby(["season", "team"]).apply(self.select_bench_players)
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
    league_offense = LeagueOffenseETL("conference", conn)
    league_offense.run()
    conn.close()
