from django.conf.urls import url

from .. import apis as views

urlpatterns = [
    url(r'^$', views.PlayList.as_view(), name='playlist-list'),
]
