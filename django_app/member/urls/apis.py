from django.conf.urls import url, include
from rest_framework.authtoken import views as auth_token_view

from member.apis.signup import SignUp_cbv
from member.apis.authtoken import DeleteAuthToken
from member.apis.login import LogoutView, LoginView

urlpatterns = [
    url(r'^signup/$', SignUp_cbv.as_view(), name='signup'),
    url(r'^token-auth/$', auth_token_view.obtain_auth_token),
    url(r'^token-delete/$', DeleteAuthToken.as_view()),

    # login url would be like this, api/memmber/login/
    url(r'^login/$', LoginView.as_view(), name='login'),
    # logout url would be like that, api/member/logout/
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'', include('rest_auth.urls')),
]
