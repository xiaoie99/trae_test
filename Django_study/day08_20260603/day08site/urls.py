from django.contrib import admin
from django.urls import path
from qyt_device.views.qyt_device_view_add_device import add_device
from qyt_device.views.qyt_device_view_show_devices import show_devices
from qyt_device.views.qyt_device_view_delete_device import delete_device
from qyt_device.views.qyt_device_view_login import qyt_login, qyt_logout
from qyt_device.views.qyt_device_view_index import index
from qyt_device.views.qyt_device_view_multi_echarts import multi_echarts
from qyt_device.views.qyt_device_view_ajax_chart2 import ajax_chart2
from qyt_device.views.qyt_device_view_ajax_pie3 import ajax_pie3
from qyt_device.views.qyt_device_view_echarts_final_line_cpu_usage import echarts_final_line_cpu_usage
from qyt_device.views.qyt_device_view_echarts_final_line_if_speed import echarts_final_line_if_speed
from qyt_device.views.qyt_device_view_ajax_final_line_cpu_usage import echarts_final_line_ajax_cpu_usage
from qyt_device.views.qyt_device_view_ajax_final_line_if_speed import echarts_final_line_ajax_if_speed_ajax
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('add_device', add_device),
    path('show_devices', show_devices),
    path('delete_device/<int:device_id>', delete_device),
    path('accounts/login', qyt_login),
    path('accounts/logout/', qyt_logout),
    path('multi_echarts', multi_echarts),
    path('ajax/chart2', ajax_chart2),
    path('ajax/pie3', ajax_pie3),
    path('echarts_final_line_cpu_usage', echarts_final_line_cpu_usage),
    path('ajax/echarts_final_line_ajax_cpu_usage', echarts_final_line_ajax_cpu_usage),
    path('echarts_final_line_if_speed', echarts_final_line_if_speed),
    path('ajax/echarts_final_line_ajax_if_speed_ajax', echarts_final_line_ajax_if_speed_ajax),
]
