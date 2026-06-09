from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from qyt_device.views.qyt_device_view_add_device import add_device
from qyt_device.views.qyt_device_view_show_devices import show_devices
from qyt_device.views.qyt_device_view_delete_device import delete_device
from qyt_device.views.qyt_device_view_login import qyt_login
from qyt_device.views.qyt_device_view_index import index
from qyt_device.views.qyt_device_view_multi_echarts import multi_echarts
from qyt_device.views.qyt_device_view_ajax_chart2 import ajax_chart2
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('add_device', add_device),
    path('show_devices', show_devices),
    path('delete_device/<int:device_id>', delete_device),
    path('accounts/login', qyt_login),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('multi_echarts', multi_echarts),
    path('ajax/chart2', ajax_chart2),
]
