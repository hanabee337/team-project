from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from search.models import Music


class MusicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = (
            # 정호 추가 pk, playlist
            'pk',
            'playlist',
            "artist",
            "title",
            "preview",
            "picture",
        )


class MusicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = (
            # 정호 추가 pk, playlist
            'pk',
            'playlist',
            "artist",
            "title",
            "preview",
            "picture",
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
