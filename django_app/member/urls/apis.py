from django.conf.urls import url, include

from member.apis.authtoken import DeleteAuthToken, ObtainAuthToken
from member.apis.login import LogoutView, LoginView, Facebook_Login_View
from member.apis.signup import SignUp_cbv, Facebook_SignUp_View
from member.apis.user import ChangePassword_View

urlpatterns = [
    url(r'^signup/$', SignUp_cbv.as_view(), name='signup'),
    url(r'^token-auth/$', ObtainAuthToken.as_view()),
    url(r'^token-delete/$', DeleteAuthToken.as_view()),

    # login url would be like this, api/memmber/login/
    url(r'^login/$', LoginView.as_view(), name='login'),
    # logout url would be like that, api/member/logout/
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    # facebook signup
    url(r'^facebook/signup/$', Facebook_SignUp_View.as_view(), name='facebook_signup'),
    # facebook login
    url(r'^facebook/login/$', Facebook_Login_View.as_view(), name='facebook_login'),

    # change password
    url(r'^changepassword/$', ChangePassword_View.as_view(), name='change_password'),

    url(r'', include('rest_auth.urls')),
]
