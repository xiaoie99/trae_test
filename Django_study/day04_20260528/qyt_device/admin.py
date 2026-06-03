from django.contrib import admin
from qyt_device.models import Devicetype
from qyt_device.models import SNMPtype
from qyt_device.models import DeviceSNMP
from qyt_device.models import Devicedb
from qyt_device.models import Devicecpu
admin.site.register(Devicetype)
admin.site.register(SNMPtype)
admin.site.register(DeviceSNMP)
admin.site.register(Devicedb)
admin.site.register(Devicecpu)
