from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from search import views

app_name = 'search'
urlpatterns = [
    url(r'^search/', views.search, name='music_search'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
