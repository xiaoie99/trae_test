from datetime import timedelta
from django.utils import timezone
from qyt_device.models import Devicecpu
def make_echarts_data(line_name, datas_list, color, shape_type='line'):
    return {
        'name': line_name,
        'symbolSize': 0,
        'data': datas_list,
        "markPoint": {
            "itemStyle": {"color": color},
            "data": [
                {"type": "max", "name": "最大值"},
                {"type": "min", "name": "最小值"},
            ],
        },
        'smooth': True,
        'type': shape_type,
        'color': color,
    }
def data_from_db(devices_list, colors_list, types_list, last_hours=10):
    last_hours_before = timezone.now() - timedelta(hours=last_hours)
    times_list = []
    name_list = []
    datas_list = []
    for device in devices_list:
        name_list.append(device.name)
        last_hours_cpu = Devicecpu.objects.filter(
            device=device,
            record_datetime__gte=last_hours_before,
        ).order_by('record_datetime')
        device_datas_list = []
        if not times_list:
            for c in last_hours_cpu:
                times_list.append(c.record_datetime.strftime('%H:%M:%S'))
                device_datas_list.append(c.cpu_usage)
        else:
            for c in last_hours_cpu:
                device_datas_list.append(c.cpu_usage)
        datas_list.append(device_datas_list)
    echarts_data_list = []
    for name, data, color, shape_type in zip(name_list, datas_list, colors_list, types_list):
        echarts_data_list.append(make_echarts_data(name, data, color, shape_type))
    return name_list, times_list, echarts_data_list
