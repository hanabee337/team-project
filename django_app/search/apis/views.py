import json
import urllib
from pprint import pprint
import json
from six.moves.urllib.request import urlopen

from awscli.compat import urlopen
from django.contrib.sites import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.status import HTTP_200_OK

from .serializers import MusicListSerializer, MusicCreateSerializer
from search.models import Music

from rest_framework.response import Response
from rest_framework import status, request, generics
from rest_framework.views import APIView
from search import models

from . import serializers

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView


# class MusicListCreate(APIView):
#     def get(self, request, format=None):
#         parameters = request.query_params
#
#         musics = models.Music.objects.all()
#         serializer = serializers.MusicListSerializer(musics, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = serializers.MusicListSerializer(data=request.data, many=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class MusicListAPIView(ListAPIView):
    serializer_class = MusicListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'artist']

    def get_queryset(self, *args, **kwargs):
        # queryset_list = super(MusicListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Music.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
        return queryset_list
#
#
class MusicCreateAPIView(CreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicCreateSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

# from django.utils.six import BytesIO
# from rest_framework.parsers import JSONParser
#
# APIVIEW로 바꾸기
# get요청을 받을 때
# get parameter중 검색어를 사용해서
# DEEzer에 요청을 하고
# 결과를 가져와서
# 그 결과로 우리쪽 db에
# 데이터를 쌓고
# 해당 데이터를 rest의 serializers를 이용해서 돌려주기

# url = 'https://api.deezer.com/2.0/search?q='
# data = {'data': 'data'}
# headers = {'type': 'track'}
#
# # r = requests.get(url, data=json.dumps(data), headers=headers)
# pprint(url)
# # answer = json.loads(r.text)
#
#
#
#
