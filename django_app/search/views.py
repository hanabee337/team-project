import json
from pprint import pprint

import requests
from django.shortcuts import render, redirect

from deezer.settings import config


def search_from_deezer(keyword, page_token=None):
    deezer_api_key = config['deezer']['API_KEY_DEEZER']
    params = {
        'q': keyword,
        'maxResults': 30,
        'type': 'artist',
        'key': deezer_api_key,
    }

    r = requests.get('https://apis.deezer.com/2.0/search?q=', params=params)
    result = r.text

    # 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
    result_dict = json.loads(result)
    return result_dict



def search(request):
    musics = []
    context = {
        'musics': musics,
    }

    keyword = request.GET.get('keyword', '').strip()

    if keyword != '':
        search_result = search_from_deezer(keyword)

        context['keyword'] = keyword

        items = search_result['data']
        pprint(items)
        for item in items:
            # 실제로 사용할 데이터
            artist = item['artist']['name']
            title = item['title']
            preview = item['preview']
            artist_picture = item['artist']['picture_small']
            album_picture = item['album']['cover_small']

            cur_item_dict = {
                'artist': artist,
                'title': title,
                'preview': preview,
                'artist_picture': artist_picture,
                'album_picture': album_picture,
            }
            musics.append(cur_item_dict)
            pprint(musics)



    return render(request, 'music/search.html', context)