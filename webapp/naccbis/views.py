from django.shortcuts import render
from django.views import View
from naccbis.models import (
    BattersOverall,
    BattersConference,
    TeamOffenseOverall,
    TeamOffenseConference,
    LeagueOffenseOverall,
    # LeagueOffenseConference,
)
from naccbis.forms import BattersInputs, TeamOffenseInputs
import Common.metrics as metrics


RENAME_COLS_OFFENSE = {
        "GO_FO": "GO/FO",
        "HBP_P": "HBP%",
        "BB_P": "BB%",
        "SO_P": "SO%",
        "X2B": "2B",
        "X3B": "3B",
        "WOBA": "wOBA",
        "WSB": "wSB",
        "WRAA": "wRAA",
        "WRC": "wRC",
        "WRC_P": "wRC+",
        "OFF_P": "OFF+",
}

ROUND_COLS_OFFENSE = {
    "go_fo": 2,
    "sar": 2,
    "hbp_p": 1,
    "bb_p": 1,
    "so_p": 1,
    "babip": 3,
    "iso": 3,
    "avg": 3,
    "obp": 3,
    "slg": 3,
    "ops": 3,
    "woba": 3,
    "wsb": 1,
    "sbr": 1,
    "wraa": 1,
    "off": 1,
    "wrc": 1,
    "wrc_p": 1,
    "off_p": 1,
    "rar": 1
}


class LeaderboardView(View):
    dashboard = ["name", "team", "season", "yr", "g", "pa", "bb_p", "so_p", "iso",
                 "babip", "avg", "obp", "slg", "woba", "wsb", "wrc_p", "off_p", "rar"]
    standard = ["name", "team", "season", "yr", "g", "pa", "ab", "x2b", "x3b", "hr",
                "r", "rbi", "bb", "so", "hbp", "sf", "sh", "gdp", "sb", "cs", "avg"]
    advanced = ["name", "team", "season", "yr", "g", "pa", "woba", "sbr", "wsb", "wraa", "off", "wrc_p", "off_p", "rar"]

    def get(self, request):
        # request parameters
        params = request.GET

        # set the form field values
        if params:
            form = BattersInputs(params)
        else:
            form = BattersInputs()

        # retrieve data from database
        if params.get("split") == "ALL":
            data = BattersOverall.objects
            totals = LeagueOffenseOverall.objects
        elif params.get("split") == "CONF":
            data = BattersConference.objects
        else:
            data = BattersOverall.objects
            totals = LeagueOffenseOverall.objects

        if params.get("min_pa"):
            data = data.filter(pa__gte=params["min_pa"])
        if params.get("team") not in ("ALL", None):
            data = data.filter(team=params["team"])
        if params.get("season") not in ("ALL", None):
            data = data.filter(season=params["season"])
            totals = totals.filter(season=params["season"])

        # convert to DataFrame
        df = data.as_dataframe()
        totals_df = totals.as_dataframe()

        # transform data
        df["name"] = list(map(lambda x, y: "{} {}".format(x, y), df["fname"], df["lname"]))
        df = metrics.multi_season(df, totals_df, metrics.season_offensive_metrics_rar)

        # select columns based on stat view
        if params.get("stat") == "DB":
            df = df[self.dashboard]
            df.sort_values("rar", ascending=False, inplace=True)
        elif params.get("stat") == "STD":
            df = df[self.standard]
            df.sort_values("avg", ascending=False, inplace=True)
        elif params.get("stat") == "ADV":
            df = df[self.advanced]
            df.sort_values("rar", ascending=False, inplace=True)
        else:
            df = df[self.dashboard]
            df.sort_values("rar", ascending=False, inplace=True)

        df.reset_index(drop=True, inplace=True)

        # round float columns
        df = df.round(ROUND_COLS_OFFENSE)
        # rename columns based on stat view
        df.columns = [col.upper() for col in df.columns.tolist()]
        df.rename(columns=RENAME_COLS_OFFENSE, inplace=True)

        context = {
            'data': df.to_html(table_id="example",
                               classes="table table-bordered table-hover",
                               index=True, na_rep=""),
            'form': form,
        }
        return render(request, 'naccbis/index.html', context)


class TeamOffenseView(View):
    dashboard = ["name", "season", "g", "pa", "bb_p", "so_p", "iso",
                 "babip", "avg", "obp", "slg", "woba", "wsb", "wrc_p", "off_p", "rar"]
    standard = ["name", "season", "g", "pa", "ab", "x2b", "x3b", "hr",
                "r", "rbi", "bb", "so", "hbp", "sf", "sh", "gdp", "sb", "cs", "avg"]
    advanced = ["name", "season", "g", "pa", "woba", "sbr", "wsb", "wraa", "off", "wrc_p", "off_p", "rar"]

    def get(self, request):
        # request parameters
        params = request.GET

        # set the form field values
        if params:
            form = TeamOffenseInputs(params)
        else:
            form = TeamOffenseInputs()

        # retrieve data from database
        if params.get("split") == "ALL":
            data = TeamOffenseOverall.objects
            totals = LeagueOffenseOverall.objects
        elif params.get("split") == "CONF":
            data = TeamOffenseConference.objects
            # totals = LeagueOffenseConference.objects
        else:
            data = TeamOffenseOverall.objects
            totals = LeagueOffenseOverall.objects

        if params.get("season") not in ("ALL", None):
            data = data.filter(season=params["season"])

        df = data.as_dataframe()
        totals_df = totals.as_dataframe()

        # transform data
        df = metrics.multi_season(df, totals_df, metrics.season_offensive_metrics_rar)

        # select columns based on stat view
        if params.get("stat") == "DB":
            df = df[self.dashboard]
            df.sort_values("rar", ascending=False, inplace=True)
        elif params.get("stat") == "STD":
            df = df[self.standard]
            df.sort_values("avg", ascending=False, inplace=True)
        elif params.get("stat") == "ADV":
            df = df[self.advanced]
            df.sort_values("rar", ascending=False, inplace=True)
        else:
            df = df[self.dashboard]
            df.sort_values("rar", ascending=False, inplace=True)

        df.reset_index(drop=True, inplace=True)

        # round float columns
        df = df.round(ROUND_COLS_OFFENSE)
        df.columns = [col.upper() for col in df.columns.tolist()]
        df.rename(columns=RENAME_COLS_OFFENSE, inplace=True)
        context = {
            'data': df.to_html(table_id="example",
                               classes="table table-bordered table-hover",
                               index=True, na_rep=""),
            'form': form,
        }
        return render(request, 'naccbis/index.html', context)
