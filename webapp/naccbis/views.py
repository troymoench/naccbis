from django.shortcuts import render
from django.views import View
from naccbis.models import BattersOverall, BattersConference, LeagueOffenseOverall
from naccbis.forms import MyForm
import Common.metrics as metrics


class LeaderboardView(View):
    dashboard = ["name", "team", "season", "yr", "g", "pa", "bb_p", "so_p", "iso",
                 "babip", "avg", "obp", "slg", "woba", "wsb", "wrc_p", "off_p", "rar"]
    standard = ["name", "team", "season", "yr", "g", "pa", "ab", "x2b", "x3b", "hr",
                "r", "rbi", "bb", "so", "hbp", "sf", "sh", "gdp", "sb", "cs", "avg"]
    advanced = ["name", "team", "season", "yr", "g", "pa", "woba", "sbr", "wsb", "wraa", "off", "wrc_p", "off_p", "rar"]

    def get(self, request):
        params = self.parse_request_params(request)

        # set the form field values
        if params:
            form = MyForm(params)
        else:
            form = MyForm()

        # retrieve data from database
        if params and params["split"] == "ALL":
            data = BattersOverall.objects.using('data')
            totals = LeagueOffenseOverall.objects.using('data')
        elif params and params["split"] == "CONF":
            data = BattersConference.objects.using('data')
        else:
            data = BattersOverall.objects.using('data')
            totals = LeagueOffenseOverall.objects.using('data')

        if params and params["min_pa"]:
            data = data.filter(pa__gte=params["min_pa"])
        if params and params["team"] != "ALL":
            data = data.filter(team=params["team"])
        if params and params["season"] != "ALL":
            data = data.filter(season=params["season"])
            totals = totals.filter(season=params["season"])

        # convert to DataFrame
        df = data.as_dataframe()
        totals_df = totals.as_dataframe()

        # transform data
        df["name"] = list(map(lambda x, y: "{} {}".format(x, y), df["fname"], df["lname"]))
        df = metrics.multi_season(df, totals_df, metrics.season_offensive_metrics_rar)

        # select columns based on stat view
        if params and params["stat"] == "DB":
            df = df[self.dashboard]
        elif params and params["stat"] == "STD":
            df = df[self.standard]
        elif params and params["stat"] == "ADV":
            df = df[self.advanced]
        else:
            df = df[self.dashboard]

        # sort
        # df.sort_values(by=["ops"], ascending=False, inplace=True)
        # df.reset_index(drop=True, inplace=True)

        # round float columns
        df = df.round({"go_fo": 2,
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
                       "wrc_p": 1,
                       "off_p": 1,
                       "rar": 1})
        # rename columns based on stat view
        df.columns = [col.upper() for col in df.columns.tolist()]
        df.rename(columns={"GO_FO": "GO/FO",
                           "HBP_P": "HBP%",
                           "BB_P": "BB%",
                           "SO_P": "SO%",
                           "X2B": "2B",
                           "X3B": "3B",
                           "WOBA": "wOBA",
                           "WSB": "wSB",
                           "WRAA": "wRAA",
                           "WRC_P": "wRC+",
                           "OFF_P": "OFF+"}, inplace=True)

        context = {'data': df.to_html(classes="table table-bordered table-hover table-sm",
                                      index=True, na_rep=""),
                   'form': form}
        return render(request, 'naccbis/index.html', context)

    def parse_request_params(self, request):
        """ Parse the request parameters """
        return request.GET
