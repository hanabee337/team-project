# Create your views here.
from pprint import pprint

import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from deezer.settings import config
from member.forms import SignupForm, LoginForm
from member.models import MyUser


def login_fbv(request):
    # return HttpResponse('login view')

    # deezer_app_id = config['deezer']['secret_key']
    # context = {
    #     'deezer_app_id': deezer_app_id,
    # }

    facebook_app_id = config['facebook']['app_id']

    # Step One: Direct your user to our authorization URL
    instagram_client_id = config['instagram']['client_id']
    context = {
        'instagram_client_id': instagram_client_id,
        'facebook_app_id': facebook_app_id,
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
        # USER_ID = dict_access_token['user']['id']
        USER_ID = dict_access_token['user']['username']
        print('USER_ID : %s' % USER_ID)

        defaults = {
            'username': dict_access_token['user']['username'],
        }
        print('defaults:{}'.format(defaults))

        user = authenticate(instagram_id=USER_ID, extra_fields=defaults)
        login(request, user)

        return redirect('index')
        # return HttpResponse('login_instagram view')


def login_facebook(request):
    # print(request.GET)
    APP_ID = config['facebook']['app_id']
    SECRET_CODE = config['facebook']['secret_code']
    REDIRECT_URI = 'http://localhost:8000/member/login/facebook/'
    APP_ACCESS_TOKEN = '{app_id}|{secret_code}'.format(
        app_id=APP_ID,
        secret_code=SECRET_CODE,
    )

    # login_fbv에서 페이스북 로그인으로 이동 후,
    # 정상적인 로그인 후 (정상적으로 로그인 시 request.GET에 'code' parameter가 추가됨)
    # redirect_uri를 이용해 다시 login_facebook으로 돌아온 후의 동작
    if request.GET.get('code'):
        # Step 1 : 사용자가 로그인 했다라는 검증
        code = request.GET.get('code')

        # Step 2 : user_access_token(사용자 액세스 토큰) 얻어오기
        # 전달받은 code 값을 이용해서 access_token값을 요청함
        # parameter들을 하기처럼 url에 직접 넣지 말 것.
        # url_request_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token?'\
        #     'client_id={app_id}'\
        #     '&redirect_uri={redirect_uri}'\
        #     '&client_secret={app_secret}'\
        #     '&code={code_parameter}'.format(
        #         app_id=app_id,
        #         app_secret=secret_code,
        #         code_parameter=code,
        #         redirect_uri=redirect_uri,
        # )

        # 하기처럼 params로 넘겨줄 것.
        url_request_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token?'
        params = {
            'client_id': APP_ID,
            'redirect_uri': REDIRECT_URI,
            'client_secret': SECRET_CODE,
            'code': code,
        }
        r = requests.get(url_request_access_token, params=params)
        pprint(r.text)
        dict_access_token = r.json()
        USER_ACCESS_TOKEN = dict_access_token['access_token']
        print('USER_ACCESS_TOKEN : %s' % USER_ACCESS_TOKEN)

        # Step 3: debug_token을 얻어오기
        # 유저 액세스 토큰과 앱 엑세스 토큰을 사용해서 토큰 검증을 거친다
        url_debug_token = 'https://graph.facebook.com/debug_token?'
        params = {
            'input_token': USER_ACCESS_TOKEN,
            'access_token': APP_ACCESS_TOKEN,
        }
        r = requests.get(url_debug_token, params=params)
        dict_debug_token = r.json()
        pprint(dict_debug_token)
        USER_ID = dict_debug_token['data']['user_id']
        print('USER_ID : %s' % USER_ID)

        # 해당 USER_ID로 graph API에 유저정보를 요청
        url_api_user = 'https://graph.facebook.com/{user_id}'.format(
            user_id=USER_ID
        )
        fields = [
            'id',
            'first_name',
            'last_name',
            'gender',
            'picture',
            'email',
        ]
        params = {
            'fields': ','.join(fields),
            'access_token': USER_ACCESS_TOKEN,
        }
        r = requests.get(url_api_user, params)
        dict_user_info = r.json()
        pprint(dict_user_info)

        first_name = dict_user_info['first_name']
        last_name = dict_user_info['last_name']
        USER_NAME = last_name + ' ' + first_name

        # 페이스북 유저 ID만으로 인증
        # user = authenticate(facebook_id=USER_ID)
        # 페이스북 유저 ID와 graph API에 요청한 dict_user_info로 인증
        user = authenticate(facebook_id=USER_NAME, extra_fields=dict_user_info)
        login(request, user)
        return redirect('index')


def signup_fbv(request):
    """
    회원 가입 구현
    1. member/signup.html 파일 생성\
    2. SignupForm 클래스 구현
    3. 해당 Form을 사용해서 signup.html템플릿 구현
    4. POST요청을 받아 MyUser객체 생성
    5. 로그인 완료되면 post_list 뷰로 이동
    """
    if request.method == 'POST':
        form = SignupForm(data=request.POST)

        if form.is_valid():
            print('form.cleaned_data:{}'.format(form.cleaned_data))

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']

            user = MyUser.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            user.gender = gender
            user.age = age
            user.save()

            print('user1:{}'.format(user))

            user = authenticate(
                username=username,
                password=password
            )
            print('user2:{}'.format(user))

            login(request=request, user=user)

            return redirect('index')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)


def login_itself(request):
    if request.method == 'POST':
        # return HttpResponse('login_itself POST view')

        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        # return HttpResponse('login_itself GET view')

        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'member/login_itself.html', context)
