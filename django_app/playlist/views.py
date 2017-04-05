from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from playlist.models import PlayList


@csrf_exempt
@login_required
def list(request):
    all_playlists = request.user.userplaylist_set.select_related('playlist')
    paginator = Paginator(all_playlists, 50)
    page = request.GET.get('page')

    try:
        playlists = paginator.page(page)
    except PageNotAnInteger:
        playlists = paginator.page(1)
    except EmptyPage:
        playlists = paginator.page(paginator.num_pages)

    context = {
        'playlists': playlists,
    }
    return render(request, 'playlist/list.html', context)


@csrf_exempt
@login_required
def playlist_making(request):
    if request.method == 'POST':
        title = request.POST['title']
        # published_date_str = request.POST['published_date']
        # published_date = parse(published_date_str)

        exist_playlist = request.user.userplaylist_set.filter(
            playlist__title=title)
        if exist_playlist:
            pass
        else:
            playlist = PlayList.objects.create(
                title=title,
                # published_date=published_date
            )
            request.user.userplaylist_set.create(
                playlist=playlist
            )
        return redirect('playlist:list')
