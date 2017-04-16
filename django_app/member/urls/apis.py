from django.conf.urls import url, include

from member.apis.authtoken import DeleteAuthToken, ObtainAuthToken
from member.apis.login import LogoutView, LoginView
from member.apis.signup import SignUp_cbv

urlpatterns = [
    url(r'^signup/$', SignUp_cbv.as_view(), name='signup'),
    url(r'^token-auth/$', ObtainAuthToken.as_view()),
    url(r'^token-delete/$', DeleteAuthToken.as_view()),

    # login url would be like this, api/memmber/login/
    url(r'^login/$', LoginView.as_view(), name='login'),
    # logout url would be like that, api/member/logout/
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'', include('rest_auth.urls')),
]
