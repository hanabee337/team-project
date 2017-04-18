from django.conf.urls import url

from .views import (
    MusicListAPIView,
    MusicCreateAPIView,
    PlayListAPIView,
)

urlpatterns = [
    url(r'^list/', MusicListAPIView.as_view(), name='music_search_list'),
    url(r'^create/', MusicCreateAPIView.as_view(), name='music_create'),
    url(r'^playlist/', PlayListAPIView.as_view(), name='search_playlist'),
]
