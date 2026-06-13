from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from qyt_device.models import Devicecpu
def line_data(name, time_data_list, color):
    return {
                'symbolSize': 0,
                'symbol': 'circle',
                'name': name,
                'type': 'line',
                'smooth': True,
                'smoothMonotone': True,
                'data': time_data_list,
                'areaStyle': {
                    'color': color
                },
                'markPoint': {
                    'itemStyle': {
                      'color': color
                    },
                    'data': [
                        {'type': 'max', 'name': '最大值'},
                        {'type': 'min', 'name': '最小值'}
                    ]
                },
                'lineStyle': {
                    'color': color
                },
                'itemStyle': {
                    'color': color
                }
            }
def change_time(datetime_obj):
    return int(datetime_obj.timestamp() * 1000)
def echarts_final_line_ajax_cpu_usage(request):
    cpu_records = list(Devicecpu.objects.filter(device__name='R1').order_by('record_datetime'))
    cpu_time_list = []
    if cpu_records:
        records = cpu_records[-24:] if len(cpu_records) >= 24 else cpu_records
        first_ts = change_time(records[0].record_datetime)
        last_ts = change_time(records[-1].record_datetime)
        if last_ts - first_ts < 60 * 1000:
            now = timezone.now()
            for i, x in enumerate(records):
                record_time = now - timedelta(minutes=(len(records) - 1 - i) * 3)
                cpu_time_list.append([change_time(record_time), x.cpu_usage])
        else:
            for x in records:
                cpu_time_list.append([change_time(x.record_datetime), x.cpu_usage])
    if cpu_time_list:
        starttime = cpu_time_list[0][0]
    else:
        starttime = '2019-12-29'
    cpu_datas = [line_data('R1 CPU利用率', cpu_time_list, '#00BFFF')]
    return JsonResponse({'labelname': 'CPU利用率',
                         'legends': [x['name'] for x in cpu_datas],
                         'datas': cpu_datas,
                         'starttime': starttime})
