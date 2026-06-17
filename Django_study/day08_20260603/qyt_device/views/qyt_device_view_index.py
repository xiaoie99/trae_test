from django.shortcuts import render
def index(request):
    return render(request, 'index.html', {'qyt_body': '强化班作业Body'})
