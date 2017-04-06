from rest_framework import generics
from rest_framework import permissions

from playlist.models import PlayList
from playlist.serializers import PlayListSerializer

__all__ = (
    'PlayList',
)


class PlayList(generics.ListCreateAPIView):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#
# class PlayListDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = PlayList.objects.all()
#     serializer_class = PlayListSerializer
