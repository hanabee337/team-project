from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from playlist.models import PlayList
from playlist.models import PlayListMusic
from playlist.serializers import PlayListSerializer, AddToMyPlayListSerializer
from search.models import Music


@api_view(['GET', 'POST'])
def select_my_playlist(request, format=None):
    q = PlayList.objects.filter(author=request.user)
    serializer = PlayListSerializer(q, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def add_to_my_playlist(request, format=None):
    playlist_id = request.data.get('playlist_id')
    music_id = request.data.get('music_id')
    playlist = PlayList.objects.get(pk=playlist_id)
    music = Music.objects.get(pk=music_id)
    # playlist.playlist_music.add(music)
    playlistmusic = PlayListMusic.objects.create(
        playlist=playlist,
        music=music,
    )
    serializer = AddToMyPlayListSerializer(playlistmusic)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

    # user = request.user
    # playlist_id = request.data.get('playlist')
    # ret = {
    #     'user': user.pk,
    #     'playlist_id': playlist_id
    # }
    # return Response(ret)
