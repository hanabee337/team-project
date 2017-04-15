from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from playlist.models import PlayList
from playlist.models import PlayListMusic
from playlist.serializers import PlayListSerializer, AddToMyPlayListSerializer
from search.models import Music

__all__ = (
    'PlayListListView',
    'PlayListDetailView',
    'select_my_playlist',
    'add_to_my_playlist',
)


class PlayListListView(generics.ListCreateAPIView):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PlayListDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    permission_classes = (permissions.IsAuthenticated,)


@api_view(['GET', 'POST'])
def select_my_playlist(request, format=None):
    if request.method == 'GET':
        playlist = PlayList.objects.filter(author=request.user.id)
        serializer = PlayListSerializer(playlist, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def add_to_my_playlist(request, format=None):
    playlist_id = request.data.get('playlist_id')
    music_song_id = request.data.get('music_song_id')
    playlist = PlayList.objects.get(pk=playlist_id)
    music = Music.objects.get(song_id=music_song_id)

    if request.method == 'POST':
        playlistmusic = PlayListMusic.objects.create(
            playlist=playlist,
            music=music,
        )
        serializer = AddToMyPlayListSerializer(playlistmusic)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
