import json

import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from search.models import Music
from search.serializers import MusicSerializer


@api_view(['GET', 'POST'])
def search(request, format=None):
    musics = []

    singers = {
        'drake', 'rick ross', 'big sean',
        'ed sheeran', 'kodak black', 'brono mars', 'sound track',
        'mastodon', 'future', 'migos', 'mercyme', 'the weeknd',
        'miranda lambert', 'keith urban', 'post malone', 'khalid'
    }

    for singer in singers:
        r = requests.get('https://api.deezer.com/search?q={}'.format(singer))
        result = r.text
        # pprint('result: {}'.format(result))
        result_dict = json.loads(result)

        search_result = result_dict
        # pprint('search_result: {}'.format(search_result))

        items = search_result['data']
        # pprint('items: {}'.format(items))

        for item in items:
            # 실제로 사용할 데이터
            id_num = item['id']
            rank = item['rank']
            duration = item['duration']
            title = item['title_short']
            artist = item['artist']['name']
            preview = item['preview']
            artist_picture_small = item['artist']['picture_small']
            artist_picture_medium = item['artist']['picture_medium']
            artist_picture_big = item['artist']['picture_big']

            album_picture_small = item['album']['cover_small']
            album_picture_medium = item['album']['cover_medium']
            album_picture_big = item['album']['cover_big']

            cur_item_dict = {
                'id_num': id_num,
                'rank': rank,
                'duration': duration,
                'artist': artist,
                'title': title,
                'preview': preview,

                'artist_picture_small': artist_picture_small,
                'artist_picture_medium': artist_picture_medium,
                'artist_picture_big': artist_picture_big,

                'album_picture_small': album_picture_small,
                'album_picture_medium': album_picture_medium,
                'album_picture_big': album_picture_big,

            }

            data = musics.append(cur_item_dict)
            # pprint('musics: {}'.format(musics))
    # jdata = musics.append(cur_item_dict)
    # bio_data = BytesIO(jdata)
    # data = JSONParser().parse(bio_data)

    if request.method == 'GET':
        musics = Music.objects.all()
        serializer = MusicSerializer(musics, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # serializer = MusicSerializer(data=request.data, many=True)
        serializer = MusicSerializer(data=musics, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
