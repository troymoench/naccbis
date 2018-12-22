from django.shortcuts import render
from django.views import View
from naccbis.models import BattersOverall, BattersConference
from naccbis.forms import MyForm
# import Cleaning.metrics as metrics


class LeaderboardView(View):
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
        elif params and params["split"] == "CONF":
            data = BattersConference.objects.using('data')
        else:
            data = BattersOverall.objects.using('data')

        if params and params["min_pa"]:
            data = data.filter(pa__gte=params["min_pa"])
        if params and params["team"] != "ALL":
            data = data.filter(team=params["team"])
        if params and params["season"] != "ALL":
            data = data.filter(season=params["season"])

        # convert to DataFrame
        df = data.as_dataframe()

        # sort
        df.sort_values(by=["ops"], ascending=False, inplace=True)
        df.reset_index(drop=True, inplace=True)

        # round float columns
        df = df.round({"go_fo": 2, "sar": 2, "hbp_p": 1, "bb_p": 1, "so_p": 1,
                       "babip": 3, "iso": 3, "avg": 3, "obp": 3, "slg": 3, "ops": 3})
        # rename / select columns based on stat view
        df.columns = [col.upper() for col in df.columns.tolist()]
        df.rename(columns={"GO_FO": "GO/FO", "HBP_P": "HBP%", "BB_P": "BB%", "SO_P": "SO%",
                           "X2B": "2B", "X3B": "3B"}, inplace=True)

        context = {'data': df.to_html(classes="table table-bordered table-hover table-sm",
                                      index=True, na_rep=""),
                   'form': form}
        return render(request, 'naccbis/index.html', context)

    def parse_request_params(self, request):
        """ Parse the request parameters """
        return request.GET
