from django.utils.translation import ugettext_lazy as _
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from member.serializers import ChangePasswordSerializer


class ChangePassword_View(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password2')
        serializer.save(password=password)
        return Response({"password": _("새 패스워드로 변경되었습니다.")}, status=status.HTTP_200_OK)
