from django.conf import settings
from django.contrib.auth import (
    logout as django_logout,
    get_user_model)
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from rest_auth.app_settings import JWTSerializer, TokenSerializer, create_token
from rest_auth.models import TokenModel
from rest_auth.utils import jwt_encode
from rest_auth.views import LoginView as RestLoginView
from rest_auth.views import LogoutView as RestLogoutView
from rest_framework import permissions
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from member.serializers import UserInfoSerializer, LoginSerializer


class LoginView(RestLoginView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework
    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel

    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data['user']

        print('login user:{}'.format(self.user))

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})

        # Get User Model
        UserModel = get_user_model()
        user = UserModel.objects.get(email__iexact=self.user.email)
        print('user: {}'.format(self.user))

        #  Serializing User Info & key
        user_info_serializer = UserInfoSerializer(user)
        print(user_info_serializer.data)
        nickname = user_info_serializer.data.get('nickname', '')
        email = user_info_serializer.data.get('email', '')
        age = user_info_serializer.data.get('age', '')
        gender = user_info_serializer.data.get('gender', '')
        key = serializer.data.get('key', '')
        user_info = {
            'nickname': nickname,
            'email': email,
            'age': age,
            'gender': gender,
            'key': key
        }
        return Response({"user_info": user_info}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()


class LogoutView(RestLogoutView):
    permission_classes = (permissions.IsAuthenticated,)

    def logout(self, request):
        print('\n RestLogoutView \n')
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({"detail": _("Token is Invalid")},
                            status=status.HTTP_400_BAD_REQUEST)

        django_logout(request)

        return Response({"detail": _("Successfully Logged-Out")},
                        status=status.HTTP_200_OK)