import json

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from playlist.models import PlayList
from playlist.models import PlayListMusic
from playlist.models.playlist import PlayListLikeUser
from playlist.serializers import PlayListLikeUserSerializer
from playlist.serializers import PlayListSerializer, AddToMyPlayListSerializer
from search.models import Music

__all__ = (
    'PlayListListView',
    'PlayListDetailView',
    'select_my_playlist',
    'add_to_my_playlist',
    'copy_others_playlist',
    'playlistlikeuser_toggle',
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
        python_playlist_id = json.loads(playlist_id)
        playlist = PlayList.objects.get(pk=python_playlist_id)
        music_song_ids = request.data.get('music_song_id')
        for music_song_id in music_song_ids:
            python_music_song_id = json.loads(music_song_id)

            music = Music.objects.get(song_id=python_music_song_id)
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

        playlist_ids = request.data.get('playlist_id')

        for playlist_id in playlist_ids:
            python_playlist_id = json.loads(playlist_id)

            playlist = PlayList.objects.get(pk=python_playlist_id)
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


@api_view(['GET', 'POST'])
def playlistlikeuser_toggle(request, format=None):
    if request.method == 'POST':
        playlist_id = request.data.get('playlist_id')
        python_playlist_id = json.loads(playlist_id)
        playlist = PlayList.objects.get(pk=python_playlist_id)
        user = request.user
        exist_playlistlikeuser = playlist.playlistlikeuser_set.filter(
            user=user,
        )
        if exist_playlistlikeuser:
            exist_playlistlikeuser.delete()
            return Response(status=status.HTTP_200_OK)

        else:
            playlistlikeuser = PlayListLikeUser.objects.create(
                playlist=playlist,
                user=user,
            )
            serializer = PlayListLikeUserSerializer(playlistlikeuser)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
