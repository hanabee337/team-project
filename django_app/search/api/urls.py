from django.conf.urls import url

from .views import (
    MusicListAPIView,
)

urlpatterns = [
    url(r'^list/', MusicListAPIView.as_view(), name='music_search_list'),
]
