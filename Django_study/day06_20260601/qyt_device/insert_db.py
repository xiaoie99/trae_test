import django
import os
import sys
import random
from datetime import timedelta
from django.utils import timezone
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day06site.settings')
django.setup()
from qyt_device.models import Devicetype, SNMPtype, DeviceSNMP, Devicedb, Devicecpu
router = Devicetype.objects.create(name='Router')
switch = Devicetype.objects.create(name='Switch')
cpu = SNMPtype.objects.create(name='CPU利用率')
DeviceSNMP.objects.create(
    device_type=router,
    snmp_type=cpu,
    oid='1.3.6.1.4.1.9.2.1.58.0',
)
r1 = Devicedb.objects.create(
    name='R1',
    ip='10.1.1.1',
    description='核心路由器',
    type=router,
    snmp_ro_community='public',
    snmp_rw_community='private',
    ssh_username='admin',
    ssh_password='cisco',
    enable_password='enable',
)
r2 = Devicedb.objects.create(
    name='R2',
    ip='10.1.1.4',
    description='备份路由器',
    type=router,
    snmp_ro_community='public',
    snmp_rw_community='private',
    ssh_username='admin',
    ssh_password='cisco',
    enable_password='enable',
)
Devicedb.objects.create(
    name='SW1',
    ip='10.1.1.2',
    description='核心交换机',
    type=switch,
    snmp_ro_community='public',
    snmp_rw_community='private',
    ssh_username='admin',
    ssh_password='cisco',
    enable_password='enable',
)
Devicedb.objects.create(
    name='R3',
    ip='10.1.1.3',
    description='分支路由器',
    type=router,
    snmp_ro_community='public',
    snmp_rw_community='private',
    ssh_username='admin',
    ssh_password='cisco',
    enable_password='enable',
)
now = timezone.now()
for i in range(24):
    record_time = now - timedelta(minutes=(23 - i) * 3)
    Devicecpu.objects.create(device=r1, cpu_usage=random.randint(5, 98), record_datetime=record_time)
    Devicecpu.objects.create(device=r2, cpu_usage=random.randint(1, 98), record_datetime=record_time)
