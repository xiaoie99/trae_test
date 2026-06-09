from django.shortcuts import render
from qyt_device.models import Devicedb
def show_devices(request, successmessage=None, errormessage=None):
    result = Devicedb.objects.all()
    devices_list = []
    for x in result:
        device_dict = {'id_delete': "/delete_device/" + str(x.id),
                       'id': x.id,
                       'name': x.name,
                       'ip': x.ip,
                       'snmp_ro_community': x.snmp_ro_community,
                       'snmp_rw_community': x.snmp_rw_community,
                       'ssh_username': x.ssh_username,
                       'ssh_password': x.ssh_password,
                       'enable_password': x.enable_password,
                       'type': x.type.name,
                       'create_datetime': x.create_datetime,
                       }
        devices_list.append(device_dict)
    return render(request, 'qyt_device_show_devices.html', {'devices_list': devices_list,
                                                            'successmessage': successmessage,
                                                            'errormessage': errormessage,
                                                            })
