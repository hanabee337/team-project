from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q


from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from .serializers import MusicListSerializer, MusicCreateSerializer
from search.models import Music

from rest_framework.response import Response
from rest_framework import status, request
from rest_framework.views import APIView
from search import models

from . import serializers


# class MusicListCreate(APIView):
#     def get(self, request, format=None):
#         musics = models.Music.objects.all()
#         serializer = serializers.MusicListSerializer(musics, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = serializers.MusicListSerializer(data=request.data, many=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#
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


class MusicCreateAPIView(CreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

# from pprint import pprint
#
# from django.contrib.sites import requests
# from django.db.models import Q
# from rest_framework import generics, filters
# from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.generics import ListAPIView
# from rest_framework.views import APIView
# from rest_framework.parsers import JSONParser
# from rest_framework.response import Response
# from music.apis.serializers import MusicSearchSerializer
# from music.models import Music
# import json
#
# from music.views import search_from_deezer
#
#
# class MusicSearchAPIView(ListAPIView, APIView):
#     serializer_class = MusicSearchSerializer
#     filter_backends = [SearchFilter, OrderingFilter]
#     search_fieldGGs = ['id', 'title', 'artist_name']
#
#     def search_from_deezer(keyword):
#         params = {
#             'q': keyword,
#             'maxResults': 20,
#             'type': 'artist',
#         }
#
#         r = requests.get('https://api.deezer.com/2.0/search?q=', params=params)
#         result = r.text
#
#
#     def search(request):
#         musics = []
#         context = {
#             'musics': musics,
#         }
#
#         keyword = request.GET.get('keyword', '').strip()
#         page_token = request.GET.get('page_token')
#
#         if keyword != '':
#             # 검색 결과를 받아옴
#             search_result = search_from_deezer(keyword, page_token)
#
#             context['keyword'] = keyword
#
#             # 검색결과에서 'items'키를 갖는 list를 items변수에 할당 후 loop
#             items = search_result['data']
#             pprint(items)
#             for item in items:
#                 # 실제로 사용할 데이터
#                 title = item['title']
#                 preview = item['preview']
#                 picture = item['album']['cover_small']
#
#                 cur_item_dict = {
#                     'title': title,
#                     'preview': preview,
#                     'picture': picture,
#                 }
#                 musics.append(cur_item_dict)
#                 pprint(cur_item_dict)
#
#         def get_queryset(self, *args, **kwargs):
#             # queryset_list = super(MusicListAPIView, self).get_queryset(*args, **kwargs)
#             # params = {
#             #     'q',
#             # }
#             # r = requests.get('https://api.deezer.com/2.0/search?q=', params=params)
#             # result = r.text
#             #
#             # # 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
#             # result_dict = json.loads(result)
#             # print(result_dict)
#             # return result_dict
#             # queryset_list = Music.objects.all()
#             queryset = cur_item_dict.objects.all()
#
#             query = queryset
#             # query = self.request.GET.get("https://api.deezer.com/2.0/search?q=mraz")
#             print(query)
#             if query:
#                 queryset_list = queryset.filter(
#                     Q(id__icontains=query) |
#                     Q(title__icontains=query) |
#                     Q(artist_name__icontains=query)
#                 ).distinct()
#             return queryset
#
#
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
