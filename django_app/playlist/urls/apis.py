from django.conf.urls import url

from .. import apis as views

urlpatterns = [
    url(r'^$', views.PlayListListView.as_view(), name='playlist-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.PlayListDetailView.as_view(), name='playlist-detail'),
]
