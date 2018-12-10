from django.shortcuts import render
from django.http import HttpResponse
from naccbis.models import BattersOverall
import pandas as pd

# Create your views here.
def index(request):

    data = BattersOverall.objects.using('data').filter(season=2018)
    data = data.filter(pa__gt=100)

    # convert to DataFrame
    fields = [field.name for field in data.model._meta.fields]
    values = [row.__dict__ for row in data]
    df = pd.DataFrame.from_records(values, columns=fields, coerce_float=True)
    df.fillna(value=pd.np.nan, inplace=True)
    # print(df)

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
                                  index=True, na_rep="")}
    return render(request, 'naccbis/index.html', context)
