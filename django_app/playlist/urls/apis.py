from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^$', apis.PlayListListView.as_view(), name='playlist-list'),
    url(r'^(?P<pk>[0-9]+)/$', apis.PlayListDetailView.as_view(), name='playlist-detail'),
]
