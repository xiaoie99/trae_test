import django
import os
import sys
import random
from datetime import timedelta
from django.utils import timezone
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day07site.settings')
django.setup()
from qyt_device.models import Devicedb, Devicecpu
r1 = Devicedb.objects.get(name='R1')
Devicecpu.objects.filter(device=r1).delete()
now = timezone.now()
for i in range(24):
    record_time = now - timedelta(minutes=(23 - i) * 3)
    obj = Devicecpu.objects.create(device=r1, cpu_usage=random.randint(1, 98))
    Devicecpu.objects.filter(pk=obj.pk).update(record_datetime=record_time)
print('R1 CPU数据已写入24条，每3分钟一条')
