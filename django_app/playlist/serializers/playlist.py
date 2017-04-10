from rest_framework import serializers

from member.serializers import UserSerializer
from playlist.models.playlist import PlayList
from search.apis.serializers import MusicListSerializer

__all__ = (
    'PlayListSerializer',
)


class PlayListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    music_set = MusicListSerializer(many=True, read_only=True)

    class Meta:
        model = PlayList
        fields = (
            'pk',
            'author',
            'title',
            'created_date',
            'music_set',
        )
        read_only_fields = (
            'created_date',
        )
