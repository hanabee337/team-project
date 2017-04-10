import json
from pprint import pprint

import requests

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from search.models import Music
from search.serializers import MusicSerializer


@api_view(['GET', 'POST'])
def search(request, format=None):
    musics = []
    context = {
        'musics': musics,
    }
    r = requests.get('https://api.deezer.com/search?q=talyor swift')
    result = r.text
    result_dict = json.loads(result)

    search_result = result_dict

    # context['keyword'] = keyword

    items = search_result['data']

    for item in items:
        # 실제로 사용할 데이터
        artist = item['artist']['name']
        title = item['title']
        preview = item['preview']
        artist_picture = item['artist']['picture_small']
        album_picture = item['album']['cover_small']

        # cur_item_dict = {
        #
        #     'artist': artist,
        #     'title': title,
        #     'preview': preview,
        #     'artist_picture': artist_picture,
        #     'album_picture': album_picture,
        #
        # }

        cur_item_dict = {

            'artist': artist,
            'title': title,
            'preview': preview,
            'artist_picture': artist_picture,
            'album_picture': album_picture,

        }


        data = musics.append(cur_item_dict)
        # print('data: {}'.format(data))
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
