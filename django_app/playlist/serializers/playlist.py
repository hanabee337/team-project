from rest_framework import serializers

from member.serializers import UserInfoSerializer
from playlist.models.playlist import PlayList, PlayListMusic, PlayListLikeUser

__all__ = (
    'PlayListSerializer',
    'AddToMyPlayListSerializer',
    'PlayListLikeUserSerializer',
)


class PlayListSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True)

    class Meta:
        model = PlayList
        fields = (
            'pk',
            'author',
            'title',
            'image',
            'playlist_music',
            'like_user',
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


class PlayListLikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayListLikeUser
        fields = (
            'pk',
            'playlist',
            'user',
            'created_date',
        )
        read_only_fields = (
            'created_date',
        )
