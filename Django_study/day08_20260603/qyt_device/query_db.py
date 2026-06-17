import django
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day08site.settings')
django.setup()
from qyt_device.models import Devicedb, DeviceSNMP, Devicecpu
print('Devicedb:')
for device in Devicedb.objects.all():
    print(device)
print('DeviceSNMP:')
for snmp in DeviceSNMP.objects.all():
    print(snmp)
print('Devicecpu:')
for cpu in Devicecpu.objects.all():
    print(cpu)
