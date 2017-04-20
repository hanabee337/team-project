from django.shortcuts import render

from playlist.models import PlayList
from playlist.models import PlayListMusic
from playlist.models.playlist import PlayListLikeUser
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

        for m in musics:
            playlistmusic = PlayListMusic.objects.create(
                playlist=playlist,
                music=m,
            )
            playlistmusics.append(playlistmusic)

        context = {
            'playlistmusics': playlistmusics,
        }
        return render(request, 'playlist/playlist.html', context)

    else:
        return render(request, 'playlist/playlist.html')


def views_copy_others_playlist(request, format=None):
    if request.method == 'POST':
        playlists = []
        copied_playlists = []
        author = request.user
        playlist_ids = request.POST.getlist('playlist_id')
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

        context = {
            'copied_playlists': copied_playlists,
        }
        return render(request, 'playlist/copy_playlist.html', context)

    else:
        return render(request, 'playlist/copy_playlist.html')


def views_playlistlikeuser_toggle(request, format=None):
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist_id')
        playlist = PlayList.objects.get(pk=playlist_id)
        user = request.user
        exist_playlistlikeuser = playlist.playlistlikeuser_set.filter(
            user=user,
        )
        if exist_playlistlikeuser:
            exist_playlistlikeuser.delete()
            toggle_status = 'Removed'
            context = {
                'user': user,
                'playlist': playlist,
                'toggle_status': toggle_status,
            }
            return render(request, 'playlist/toggle_playlistlike.html', context)


        else:
            playlistlikeuser = PlayListLikeUser.objects.create(
                playlist=playlist,
                user=user,
            )
            toggle_status = 'Toggled'
            context = {
                'user': user,
                'playlist': playlist,
                'toggle_status': toggle_status,
                'playlistlikeuser': playlistlikeuser,
            }
            return render(request, 'playlist/toggle_playlistlike.html', context)

    else:
        return render(request, 'playlist/toggle_playlistlike.html')
