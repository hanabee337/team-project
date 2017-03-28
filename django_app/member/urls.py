from django.conf.urls import url

from . import views

app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.login_fbv, name='login'),
    url(r'^logout/$', views.logout_fbv, name='logout'),

    url(r'^login/deezer/$', views.login_deezer, name='login_deezer'),

    url(r'^login/instagram/$', views.login_instagram, name='login_instagram'),
]
