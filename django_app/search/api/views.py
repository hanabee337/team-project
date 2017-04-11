from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView

from search.models import Music
from .serializers import MusicListSerializer, MusicCreateSerializer


class MusicListAPIView(ListAPIView):
    serializer_class = MusicListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'artist']

    # def list(self, request, *args, **kwargs):
    #     # 우리db에서 리스트 결과를 돌려주기전에 해야할 일을 추가
    #     # request.query_params
    #     # request.data
    #     return super().list(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
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

    def perform_create(self, serializer):
        serializer.save()
