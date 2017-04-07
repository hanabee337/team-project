from django.conf.urls import url

from .views import (
    MusicListAPIView,
    # MusicListCreate,
    MusicCreateAPIView)

urlpatterns = [
    url(r'^list/$', MusicListAPIView.as_view(), name='music_list'),
    url(r'^create/$', MusicCreateAPIView.as_view(), name='music_create'),

]
