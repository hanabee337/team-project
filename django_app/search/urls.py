from django.conf.urls import url

from .views import (
    # MusicListAPIView,
    MusicListCreate,
    MyApi,
    PartyView)

urlpatterns = [
    url(r'^list/$', MusicListCreate.as_view(), name='music_list'),
    url(r'^create/$', MusicListCreate.as_view(), name='music_create'),
    url(r'^myapi/$', MyApi.as_view(), name='music_create'),
    url(r'^party/$', PartyView.as_view(), name='music_create'),

]
