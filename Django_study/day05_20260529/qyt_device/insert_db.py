import django
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day05site.settings')
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
Devicecpu.objects.create(device=r1, cpu_usage=30)
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
