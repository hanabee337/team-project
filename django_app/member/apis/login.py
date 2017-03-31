from django.contrib.auth import (
    logout as django_logout
)
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from rest_auth.views import LogoutView as RestLogoutView
from rest_framework import status
from rest_framework.response import Response


# class LoginView(GenericAPIView):
#     pass


class LogoutView(RestLogoutView):
    def logout(self, request):

        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({"detail": _("Token is Invalid")},
                            status=status.HTTP_400_BAD_REQUEST)

        django_logout(request)

        return Response({"detail": _("Successfully Logged-Out")},
                        status=status.HTTP_200_OK)
