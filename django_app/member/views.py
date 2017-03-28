# Create your views here.
from pprint import pprint

import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from deezer.settings import config


def login_fbv(request):
    # return HttpResponse('login view')

    # deezer_app_id = config['deezer']['secret_key']
    # context = {
    #     'deezer_app_id': deezer_app_id,
    # }


    # Step One: Direct your user to our authorization URL
    instagram_client_id = config['instagram']['client_id']
    context = {
        'instagram_client_id': instagram_client_id,
    }
    return render(request, 'member/login.html', context)


def logout_fbv(request):
    logout(request)
    return redirect('index')


def login_deezer(request):
    print(request.GET)
    return HttpResponse('login_deezer view')


def login_instagram(request):
    print('request.GET:{}'.format(request.GET))

    CLIENT_ID = config['instagram']['client_id']
    CLIENT_SECRET = config['instagram']['client_secret']
    GRANT_TYPE = 'authorization_code'
    REDIRECT_URI = 'http://localhost:8000/member/login/instagram'

    # Step Two: Receive the redirect from Instagram with 'code' parameters
    if request.GET.get('code'):
        code = request.GET.get('code')
        print(code)

        # Step Three: Request the access_token with 'code'
        url_access_token = 'https://api.instagram.com/oauth/access_token'
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': GRANT_TYPE,
            'redirect_uri': REDIRECT_URI,
            'code': code,
        }

        r = requests.post(url=url_access_token, data=data)
        print(r)
        dict_access_token = r.json()
        pprint(dict_access_token)
        USER_ID = dict_access_token['user']['id']
        print('USER_ID : %s' % USER_ID)

        defaults = {
            'username': dict_access_token['user']['username'],
        }
        print('defaults:{}'.format(defaults))

        user = authenticate(instagram_id=USER_ID, extra_fields=defaults)
        login(request, user)

        return redirect('index')
        # return HttpResponse('login_instagram view')
