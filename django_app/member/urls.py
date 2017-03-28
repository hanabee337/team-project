from django.conf.urls import url

from . import views

app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.login_fbv, name='login'),

    url(r'^login/deezer/$', views.login_deezer, name='login_deezer'),
]