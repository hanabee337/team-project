from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        # print('request.data:{}'.format(request.data))

        # First, validate request.data in SignupSerializer
        signup_serializer = self.get_serializer(data=request.data)
        signup_serializer.is_valid(raise_exception=True)
        # print('\nsignup_serializer.validated_data:{}\n'.format(signup_serializer.validated_data))
        self.perform_create(signup_serializer)

        user = User_model.objects.get(email__iexact=request.data.get('email'))
        user_info = {
            'email': user.email,
            'nickname': user.nickname,
            'user_type': user.user_type,
        }
        # print('user_info:{}'.format(user_info))

        # print('Facebook_SignUp_View:{}'.format(data))
        return Response({'user_info': user_info}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # print('\nperform_create\n')
        # facebook userid 검증(?)
        serializer.save()
