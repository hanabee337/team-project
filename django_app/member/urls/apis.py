from django.conf.urls import url, include
from rest_framework.authtoken import views as auth_token_view

from member.apis.login import LogoutView
from .. import apis as views

urlpatterns = [
    url(r'^signup/$', views.SignUp_cbv.as_view(), name='signup'),
    url(r'^token-auth/$', auth_token_view.obtain_auth_token),

    # login url would be like this, api/memmber/login/
    # logout url would be like that, api/member/logout/
    url(r'^logout/$', LogoutView.as_view()),
    url(r'', include('rest_auth.urls')),
]
