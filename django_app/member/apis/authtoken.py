from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class DeleteAuthToken(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        print(request.auth)
        print(type(request.auth))
        token = Token.objects.get(key=request.auth.key)
        print('token:{}'.format(token))
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
