"""deezer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

import search.apis.urls
from member.urls import apis as member_apis_urls
from playlist.urls import apis as playlist_apis_urls
from . import views

api_urlpatterns = [
    url(r'^member/', include(member_apis_urls)),
    # 정호 추가
    url(r'^playlist/', include(playlist_apis_urls)),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # local-server용 urls
    url(r'^$', views.index, name='index'),
    url(r'^playlist/', include('playlist.urls')),

    # api용 urls
    url(r'^apis/', include(api_urlpatterns, namespace='apis')),

    # apis/search urls
    url(r'^apis-search/', include(search.apis.urls, namespace='apis-search')),
]
