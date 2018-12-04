from django.shortcuts import render
from django.http import HttpResponse
from .models import RawBattersOverall


# Create your views here.
def index(request):

    data = RawBattersOverall.objects.using('data').filter(season=2018)
    data = data.filter(pa__gt=100)

    for row in data:
        row.calc_ops()

    print(request.GET.get("sort"))
    sort_param = request.GET.get("sort")
    # print(sort_param.split(","))
    if sort_param is not None:
        # data = data.order_by("-pa")
        descending = True
        if len(sort_param.split(",")) > 1:
            descending = sort_param.split(",")[1] != "a"
        data = sorted(data, key=lambda x: getattr(x, sort_param.split(",")[0]), reverse=descending)
    else:
        data = sorted(data, key=lambda x: x.ops, reverse=True)

    context = {'data': data}
    return render(request, 'naccbis/index.html', context)
