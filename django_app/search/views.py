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
        # 'Ed Sheeran', 'Zara Larsson', 'Clean Bandit', 'Drake', 'Bruno Mars', 'The Chainsmokers', 'The Weeknd',
        # 'Trolls [2016]', 'Justin Bieber', 'Coldplay', 'Adele', 'Selena Gomez', 'Taylor Swift', 'Alessia Cara',
        # 'Kygo',
        'alicia keys',
    }

    for singer in singers:
        initial_r = requests.get('https://api.deezer.com/search?q={}'.format(singer))
        result = initial_r.text
        result_dict = json.loads(result)
        search_result = result_dict
        total_results = search_result['total']
        print(total_results)

        page_num = 0
        while page_num < total_results:
            starting_r = requests.get('https://api.deezer.com/search?q={}&index={}'.format(singer, page_num))

            result = starting_r.text
            result_dict = json.loads(result)

            search_result = result_dict
            total_results = search_result['total']

            items = search_result['data']

            for item in items:
                # 실제로 사용할 데이터
                song_id = item['id']
                rank = item['rank']
                duration = item['duration']
                title = item['title_short']
                artist = item['artist']['name']
                preview = item['preview']
                artist_picture_small = item['artist']['picture_small']
                artist_picture_medium = item['artist']['picture_medium']
                artist_picture_big = item['artist']['picture_big']

                album_id = item['album']['id']
                album_title = item['album']['title']
                album_picture_small = item['album']['cover_small']
                album_picture_medium = item['album']['cover_medium']
                album_picture_big = item['album']['cover_big']

                cur_item_dict = {
                    'song_id': song_id,
                    'rank': rank,
                    'duration': duration,
                    'artist': artist,
                    'title': title,
                    'preview': preview,

                    'artist_picture_small': artist_picture_small,
                    'artist_picture_medium': artist_picture_medium,
                    'artist_picture_big': artist_picture_big,

                    'album_id': album_id,
                    'album_title': album_title,
                    'album_picture_small': album_picture_small,
                    'album_picture_medium': album_picture_medium,
                    'album_picture_big': album_picture_big,
                }
                data = musics.append(cur_item_dict)

            page_num += 25

    if request.method == 'GET':
        musics = Music.objects.all()
        serializer = MusicSerializer(musics, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MusicSerializer(data=musics, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
