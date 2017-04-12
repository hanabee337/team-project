from rest_framework import serializers

from member.serializers import UserInfoSerializer
from playlist.models.playlist import PlayList, PlayListMusic

__all__ = (
    'PlayListSerializer',
    'AddToMyPlayListSerializer',
)


class PlayListSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True)
    # music_set = MusicListSerializer(many=True, read_only=True)

    class Meta:
        model = PlayList
        fields = (
            'pk',
            'author',
            'title',
            'image',
            'playlist_music',
        )
        read_only_fields = (
            # 'author',
        )
        depth = 1


class AddToMyPlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayListMusic
        fields = (
            'pk',
            'playlist',
            'music',
            'created_date',
        )
        read_only_fields = (
            'created_date',
        )
