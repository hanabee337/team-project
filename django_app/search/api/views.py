from django.db.models import Q
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

from search.models import Music
from .serializers import MusicListSerializer, MusicCreateSerializer


class MusicListAPIView(ListAPIView):
    serializer_class = MusicListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'artist', 'album_id', 'song_id']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Music.objects.distinct('song_id')
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(artist__icontains=query) |
                Q(album_id__icontains=query)
            ).distinct()
        return queryset_list


class MusicCreateAPIView(CreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

