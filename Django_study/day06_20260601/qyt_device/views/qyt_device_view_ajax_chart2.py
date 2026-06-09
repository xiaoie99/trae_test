from django.http import JsonResponse
from qyt_device.models import Devicedb
from qyt_device.views.qyt_device_view_make_echarts_data import data_from_db
def ajax_chart2(request):
    all_data = data_from_db(Devicedb.objects.filter(name__in=['R1', 'R2']).order_by('name'),
                            ['#00BFFF', '#FF3300'],
                            ['bar', 'line'])
    return JsonResponse({
        'labelname': 'CPU利用率',
        'legends': all_data[0],
        'labels': all_data[1],
        'datas': all_data[2],
    })
