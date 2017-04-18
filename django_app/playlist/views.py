from django.shortcuts import render

from playlist.models import PlayList
from playlist.models import PlayListMusic
from search.models import Music


def views_add_to_my_playlist(request, format=None):
    if request.method == 'POST':
        musics = []
        playlistmusics = []
        playlist_id = request.POST.get('playlist_id')
        music_song_ids = request.POST.getlist('music_song_id')

        playlist = PlayList.objects.get(pk=playlist_id)

        for music_song_id in music_song_ids:
            music = Music.objects.get(song_id=music_song_id)
            musics.append(music)

        for music in musics:
            playlistmusic = PlayListMusic.objects.create(
                playlist=playlist,
                music=music,
            )
            playlistmusics.append(playlistmusic)
        context = {
            'playlistmusics': playlistmusics,
        }
        return render(request, 'playlist/playlist.html', context)

    else:
        return render(request, 'playlist/playlist.html')
