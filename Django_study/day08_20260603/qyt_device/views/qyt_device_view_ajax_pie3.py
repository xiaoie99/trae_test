from django.http import JsonResponse
import random
def ajax_pie3(request):
    pie3_label = '协议分布'
    pie3_protocol = ['HTTP', 'Telnet', 'SSH', 'ICMP']
    pie3_data = [{'value': random.randint(20, 100), 'name': p} for p in pie3_protocol]
    return JsonResponse({'labelname': pie3_label,
                         'labels': pie3_protocol,
                         'datas': pie3_data})
