from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from member.serializers import SignupSerializer


class SignUp_cbv(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        # 회원 가입하면서 gender, age, email 등을 동시에 입력하는 실습
        # request.data : name, password, email, gender, age + user.pk
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print('dir(serializer.data):{}'.format(dir(serializer.data)))

        ret = serializer.data
        print('serializer.data:{}'.format(serializer.data))

        user_info = {
            'username': ret.get('username', ''),
            'email': ret.get('email', ''),
            'age': ret.get('age', ''),
            'nickname': ret.get('nickname', ''),
            'gender': ret.get('gender', '')
        }

        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'user_info': user_info}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
