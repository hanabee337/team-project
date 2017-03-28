from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):
    # return HttpResponse('index')
    # return redirect('member:login')
    return render(request, 'common/index.html')
