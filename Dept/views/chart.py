from django.http import JsonResponse
from django.shortcuts import render


def chart_list(request):

    return render(request, "chart_list.html")


def chart_bar(request):

    legend = ['销量']
    series_list = [{
            "name": legend,
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
          }]
    x_axis = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }
    }

    return JsonResponse(result)