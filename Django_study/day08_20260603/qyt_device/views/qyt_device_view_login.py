from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
def qyt_login(request):
    error = ''
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or request.GET.get('next') or '/'
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            request.session['fname'] = request.user.first_name
            request.session['device_permission'] = False
            employee_group = Group.objects.filter(name='employee').first()
            if employee_group and employee_group in user.groups.all():
                request.session['device_permission'] = True
            elif 'qyt_device.view_devicedb' in request.user.get_all_permissions():
                request.session['device_permission'] = True
            return redirect(next_url)
        error = '用户名或密码错误'
    return render(request, 'registration/login.html', {'error': error, 'next': next_url})
def qyt_logout(request):
    logout(request)
    return redirect('/')
