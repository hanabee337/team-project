from pprint import pprint

import requests
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from deezer import settings
from member.serializers import UserSerializer, SignupSerializer, Facebook_SignUp_Serializer

User_model = get_user_model()


class SignUp_cbv(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        # print('\nSignUp_cbv create\n')

        # First, validate request.data in SignupSerializer
        signup_serializer = self.get_serializer(data=request.data)
        signup_serializer.is_valid(raise_exception=True)
        # print('\nsignup_serializer.validated_data:{}\n'.format(signup_serializer.validated_data))

        # After everything is confirmed as valid,
        # then, send it to UserSerializer
        model_serializer = UserSerializer(data=signup_serializer.data)
        # print('\nmodel_serializer.initial_data:{}\n'.format(model_serializer.initial_data))

        # model_serializer 에서는 password2는 skip 하고,
        # password1은 password 로 변경(UserSerializer 에서 field 로 정의한)한 후,
        # validation 하여 model_serializer.data 값을 얻는다.
        model_serializer.initial_data = {
            'password': signup_serializer.data.get('password1'),
            'email': signup_serializer.data.get('email'),
            'nickname': signup_serializer.data.get('nickname'),
            'gender': signup_serializer.data.get('gender'),
            'age': signup_serializer.data.get('age'),
        }
        # print('\nmodel_serializer.initial_data:{}\n'.format(model_serializer.initial_data))

        model_serializer.is_valid(raise_exception=True)
        # print('\nmodel_serializer.data:{}\n'.format(model_serializer.data))

        # UserSerializer 에서 '.save()' 실행하고, 'create_user'를 진행한다.
        self.perform_create(model_serializer)

        headers = self.get_success_headers(model_serializer.data)

        ret = model_serializer.data
        user_info = {
            'email': ret.get('email', ''),
            'age': ret.get('age', ''),
            'nickname': ret.get('nickname', ''),
            'gender': ret.get('gender', ''),
            'user_type': ret.get('user_type'),
        }

        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'user_info': user_info}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # print('\nperform_create\n')
        serializer.save()


class Facebook_SignUp_View(generics.CreateAPIView):
    serializer_class = Facebook_SignUp_Serializer

    def post(self, request, *args, **kwargs):
        # print('post request.data:{}'.format(request.data))
        if User_model.objects.filter(email__iexact=request.data.get('email')).exists():
            # 이미 있으면 여기서 로그인 루틴 처리(로그인, Token 반환, authenticate)
            return Response({'이미 등록된 가입자 입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # print('CREATE request.data:{}'.format(request.data))

        APP_ID = settings.config['facebook']['app_id']
        SECRET_CODE = settings.config['facebook']['secret_code']
        # REDIRECT_URI = 'http://localhost:8000/member/login/facebook/'
        APP_ACCESS_TOKEN = '{app_id}|{secret_code}'.format(
            app_id=APP_ID,
            secret_code=SECRET_CODE,
        )
        USER_ACCESS_TOKEN = request.data.get('email')

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

        if dict_debug_token['data']['is_valid']:
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

            # First, validate request.data in SignupSerializer
            signup_serializer = self.get_serializer(data=request.data)

            # user id가 unique 하므로, email 과 password 로 활용
            # signup_serializer.initial_data['email'] = USER_ID
            # signup_serializer.initial_data['password'] = USER_ID
            signup_serializer.initial_data = {
                'email': USER_ID,
                'password': USER_ID,
                'nickname': request.data.get('nickname'),
                # 'gender': request.data.get('gender', ''),
                # 'age': request.data.get('age', '')
            }

            signup_serializer.is_valid(raise_exception=True)
            # print('\n signup_serializer.validated_data:{}\n'.format(signup_serializer.validated_data))

            # access token 을 email 란으로 입력 받은 후, 다시 user id로 바꿔치기.

            if User_model.objects.filter(email__iexact=USER_ID).exists():
                # 로그인 루틴을 여기서 처리하는 것으로..
                # 회원 가입과 로그인(Token key 생성, password check)을 하나의 url에서 처리하게...
                return Response({'이미 가입된 사용자 입니다.'}, status=status.HTTP_400_BAD_REQUEST)

            self.perform_create(signup_serializer)

            user = User_model.objects.get(email__iexact=USER_ID)
            user_info = {
                'email': user.email,
                'nickname': user.nickname,
                'user_type': user.user_type,
                'gender': user.gender,
                'age': user.age,
            }
            print('user_info:{}'.format(user_info))
            # print('Facebook_SignUp_View:{}'.format(data))
            return Response({'user_info': user_info}, status=status.HTTP_201_CREATED)
        else:
            return Response({'Facebook에서 유효한 User ID를 얻는데 실패했습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # print('\n perform_create\n')
        serializer.save()
