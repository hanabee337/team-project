from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView

from search.models import Music
from .serializers import MusicListSerializer


class MusicListAPIView(ListAPIView):
    serializer_class = MusicListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'artist']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Music.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
        return queryset_list
