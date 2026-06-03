from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from qyt_device.views.qyt_device_view_add_device import add_device
from qyt_device.views.qyt_device_view_login import qyt_login
from qyt_device.views.qyt_device_view_index import index
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('add_device', add_device),
    path('accounts/login', qyt_login),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
