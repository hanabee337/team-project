from rest_framework import serializers

from search.models import Music


class MusicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = (
            "song_id",
            "rank",
            "duration",
            "artist",
            "title",
            "preview",

            "artist_picture_small",
            "artist_picture_medium",
            "artist_picture_big",

            "album_id",
            "album_title",
            "album_picture_small",
            "album_picture_medium",
            "album_picture_big",
        )


class MusicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = (
            "song_id",
            "rank",
            "duration",
            "artist",
            "title",
            "preview",

            "artist_picture_small",
            "artist_picture_medium",
            "artist_picture_big",

            "album_id",
            "album_title",
            "album_picture_small",
            "album_picture_medium",
            "album_picture_big",
        )

