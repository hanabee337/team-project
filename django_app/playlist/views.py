from django.shortcuts import render

from playlist.models import PlayList
from playlist.models import PlayListMusic
from search.models import Music


def views_add_to_my_playlist(request, format=None):
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist_id')
        music_id_num = request.POST.get('music_id_num')
        playlist = PlayList.objects.get(pk=playlist_id)
        music = Music.objects.get(id_num=music_id_num)
        playlistmusic = PlayListMusic.objects.create(
            playlist=playlist,
            music=music,
        )
        context = {
            'playlistmusic': playlistmusic,
        }
        return render(request, 'playlist/playlist.html', context)

    else:
        return render(request, 'playlist/playlist.html')
