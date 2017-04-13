from rest_framework import serializers

from search.models import Music


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('song_id', 'rank', 'duration', 'title', 'artist', 'preview',
                  'artist_picture_small', 'artist_picture_medium', 'artist_picture_big',

                  'album_id', 'album_title',
                  'album_picture_small', 'album_picture_medium', 'album_picture_big',)
