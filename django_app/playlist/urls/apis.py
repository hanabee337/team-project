from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from playlist import views
from .. import apis

urlpatterns = [
    url(r'^$', apis.PlayListListView.as_view(), name='playlist-list'),
    url(r'^(?P<pk>[0-9]+)$', apis.PlayListDetailView.as_view(), name='playlist-detail'),
    url(r'^select_my_playlist', apis.select_my_playlist),
    url(r'^add_to_my_playlist', apis.add_to_my_playlist),
    url(r'^copy_others_playlist', apis.copy_others_playlist),
    url(r'^playlistlikeuser_toggle', apis.playlistlikeuser_toggle),

    url(r'^views_add_to_my_playlist', views.views_add_to_my_playlist),
    url(r'^views_copy_others_playlist', views.views_copy_others_playlist),
    url(r'^views_playlistlikeuser_toggle', views.views_playlistlikeuser_toggle),

]

urlpatterns = format_suffix_patterns(urlpatterns)
