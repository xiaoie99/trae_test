from django.views.decorators.http import require_POST
from qyt_device.views.qyt_device_view_show_devices import show_devices
from qyt_device.models import Devicedb
@require_POST
def delete_device(request, device_id):
    try:
        m = Devicedb.objects.get(id=device_id)
        m.delete()
        return show_devices(request, successmessage="设备删除成功")
    except Devicedb.DoesNotExist:
        return show_devices(request, errormessage="设备未找到!或者已经被删除!")
