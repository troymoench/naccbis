from django.shortcuts import render
from django.http import HttpResponse
from naccbis.models import BattersOverall, PlayerId
from naccbis.forms import MyForm
import pandas as pd
# import Cleaning.metrics as metrics


# Create your views here.
def index(request):
    # parse the request parameters
    filter_team = request.GET.get("team")
    filter_pa = request.GET.get("min_pa")
    filter_season = request.GET.get("season")
    # set the form field values
    if filter_team or filter_pa or filter_season:
        form = MyForm({"team": filter_team, "min_pa": filter_pa, "season": filter_season})
    else:
        form = MyForm()

    player_id = PlayerId.objects.using('data')
    data = BattersOverall.objects.using('data')
    if filter_pa:
        data = data.filter(pa__gte=filter_pa)
    if filter_team and filter_team != "ALL":
        data = data.filter(team=filter_team)
    if filter_season and filter_season != "ALL":
        data = data.filter(season=filter_season)

    # convert to DataFrame
    ids = player_id.as_dataframe()
    df = data.as_dataframe()

    df = ids.merge(df)
    # sort
    df.sort_values(by=["ops"], ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # print(request.GET.get("sort"))
    # sort_param = request.GET.get("sort")
    # # print(sort_param.split(","))
    # if sort_param is not None:
    #     # data = data.order_by("-pa")
    #     descending = True
    #     if len(sort_param.split(",")) > 1:
    #         descending = sort_param.split(",")[1] != "a"
    #     data = sorted(data, key=lambda x: getattr(x, sort_param.split(",")[0]), reverse=descending)
    # else:
    #     data = sorted(data, key=lambda x: x.ops, reverse=True)

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
