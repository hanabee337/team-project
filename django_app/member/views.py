# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from deezer.settings import config


def login_fbv(request):
    # return HttpResponse('login view')

    deezer_app_id = config['deezer']['secret_key']
    context = {
        'deezer_app_id': deezer_app_id,
    }
    return render(request, 'member/login.html', context)


def login_deezer(request):
    print(request.GET)
    return HttpResponse('login_deezer view')
