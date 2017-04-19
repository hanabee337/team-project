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
    'copy_others_playlist',
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
    if request.method == 'POST':
        musics = []
        playlistmusics = []
        playlist_id = request.data.get('playlist_id')
        music_song_ids = request.data.getlist('music_song_id')

        playlist = PlayList.objects.get(pk=playlist_id)

        for music_song_id in music_song_ids:
            music = Music.objects.get(song_id=music_song_id)
            musics.append(music)

            for m in musics:
                playlistmusic = PlayListMusic.objects.create(
                    playlist=playlist,
                    music=m,
                )
                playlistmusics.append(playlistmusic)
            serializer = AddToMyPlayListSerializer(playlistmusics, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def copy_others_playlist(request, format=None):
    if request.method == 'POST':
        playlists = []
        copied_playlists = []
        author = request.user
        playlist_ids = request.data.getlist('playlist_id')
        for playlist_id in playlist_ids:
            playlist = PlayList.objects.get(pk=playlist_id)
            playlists.append(playlist)

        for p in playlists:
            title = p.title
            image = p.image
            musics = p.playlist_music.all()
            copied_playlist = PlayList.objects.create(
                author=author,
                title=title,
                image=image,
            )

            for m in musics:
                PlayListMusic.objects.create(
                    playlist=copied_playlist,
                    music=m,
                )
            copied_playlists.append(copied_playlist)
        serializer = PlayListSerializer(copied_playlists, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
