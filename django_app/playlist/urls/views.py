from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from playlist import views

urlpatterns = [
    url(r'^select_my_playlist', views.select_my_playlist),
    url(r'^add_to_my_playlist', views.add_to_my_playlist),
]

urlpatterns = format_suffix_patterns(urlpatterns)
