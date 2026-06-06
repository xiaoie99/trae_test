from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
def qyt_login(request):
    error = ''
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or request.GET.get('next') or '/'
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['device_permission'] = True
            return redirect(next_url)
        error = '用户名或密码错误'
    return render(request, 'registration/login.html', {'error': error, 'next': next_url})
