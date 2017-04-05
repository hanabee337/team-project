from django.conf.urls import url

from . import views

app_name = 'playlist'
urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^playlist_making/$', views.playlist_making, name='playlist_making'),
]
