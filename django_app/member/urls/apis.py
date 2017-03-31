from django.conf.urls import url

from .. import apis as views

urlpatterns = [
    url(r'^signup/$', views.SignUp_cbv.as_view(), name='signup'),
]
