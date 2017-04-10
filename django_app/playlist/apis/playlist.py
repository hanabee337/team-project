from rest_framework import generics
from rest_framework import permissions

from playlist.models import PlayList
from playlist.serializers import PlayListSerializer

__all__ = (
    'PlayListListView',
    'PlayListDetailView',
)


class PlayListListView(generics.ListCreateAPIView):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PlayListDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
