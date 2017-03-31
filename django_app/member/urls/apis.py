from django.conf.urls import url
from rest_framework.authtoken import views as auth_token_view

from .. import apis as views

urlpatterns = [
    url(r'^signup/$', views.SignUp_cbv.as_view(), name='signup'),
    url(r'^token-auth/', auth_token_view.obtain_auth_token)
]
