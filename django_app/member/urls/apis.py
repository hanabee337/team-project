from django.conf.urls import url

from .. import apis as views

urlpatterns = [
    url(r'^$', views.MemberView.as_view(), name='memberview'),
]
