from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from search import views


urlpatterns = [
    url(r'^$', views.search, name='music_search'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
