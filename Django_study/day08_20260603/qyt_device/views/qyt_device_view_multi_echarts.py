from django.shortcuts import render
from qyt_device.models import Devicedb
from qyt_device.views.qyt_device_view_make_echarts_data import data_from_db
import json
import random
def multi_echarts(request):
    all_data = data_from_db(Devicedb.objects.filter(name__in=['R1', 'R2']).order_by('name'),
                            ['#00BFFF', '#FF3300'],
                            ['bar', 'line'],
                            last_hours=10)
    pie2_label = '协议分布'
    pie2_protocol = ['HTTP', 'Telnet', 'SSH', 'ICMP']
    pie2_data = [{'value': random.randint(20, 100), 'name': p} for p in pie2_protocol]
    return render(request, 'qyt_device_multi_echarts.html', {
        'chart2_label': 'CPU利用率',
        'chart2_legends': json.dumps(all_data[0]),
        'chart2_time': json.dumps(all_data[1]),
        'chart2_data': json.dumps(all_data[2]),
        'pie2_label': json.dumps(pie2_label),
        'pie2_protocol': json.dumps(pie2_protocol),
        'pie2_data': json.dumps(pie2_data),
    })
