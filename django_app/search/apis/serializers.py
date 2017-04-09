from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from search.models import Music


class MusicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = (
        "id_num",
        "rank",
        "duration",
        "title",
        "artist",
        "preview",

        "artist_picture_small",
        "artist_picture_medium",
        "artist_picture_big",

        "album_picture_small",
        "album_picture_medium",
        "album_picture_big",
        )


class MusicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = (
            "id_num",
            "rank",
            "duration",
            "title",
            "artist",
            "preview",

            "artist_picture_small",
            "artist_picture_medium",
            "artist_picture_big",

            "album_picture_small",
            "album_picture_medium",
            "album_picture_big",
        )


# from rest_framework import serializers
#
# from music.models import Music
#
#
# class MusicSearchSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Music
#         fields = [
#             'id',
#             'title',
#             'preview',
#             'picture',
#         ]
#
#
#     def create(self, validated_data):
#         music, created = Music.objects.get_or_create(
#             title=validated_data['title'],
#             # phone=validated_data['phone'],
#             defaults={
#                 'title': validated_data['title'],
#                 # 'last_name': validated_data['last_name']
#             })
#
#         return music
#
