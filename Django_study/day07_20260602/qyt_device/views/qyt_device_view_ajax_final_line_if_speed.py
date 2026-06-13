from django.http import JsonResponse
from django.utils import timezone
import datetime
import random
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
    if timezone.is_naive(datetime_obj):
        datetime_obj = timezone.make_aware(datetime_obj, timezone.get_current_timezone())
    return int(datetime_obj.timestamp() * 1000)
def echarts_final_line_ajax_if_speed_ajax(request):
    g1_up_time_speed_list = []
    g1_down_time_speed_list = []
    now_time = timezone.now()
    for i in range(1000):
        point_time = now_time - datetime.timedelta(minutes=(999 - i) * 30)
        g1_up_time_speed_list.append(
            [change_time(point_time),
             random.randint(40, 60)])
        g1_down_time_speed_list.append(
            [change_time(point_time),
             random.randint(30, 70)])
    speed_datas = [line_data('G1 up流量', g1_up_time_speed_list, '#00BFFF'),
                   line_data('G1 down流量', g1_down_time_speed_list, '#FF3300')]
    starttime = change_time(now_time - datetime.timedelta(minutes=999 * 30))
    return JsonResponse({'labelname': '接口速率',
                         'legends': [x['name'] for x in speed_datas],
                         'datas': speed_datas,
                         'starttime': starttime})
