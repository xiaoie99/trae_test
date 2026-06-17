from django.shortcuts import render
def echarts_final_line_cpu_usage(request):
    return render(request, 'qyt_device_echarts_final_line_cpu_usage.html')
