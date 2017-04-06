from rest_framework import serializers

from member.serializers import UserSerializer
from playlist.models import PlayList


class PlayListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = PlayList
        fields = (
            'pk',
            'author',
            'title',
            'playlist_music',
            # 'created_date',
        )
        read_only_fields = (
            'title',
            'playlist_music',
            # 'created_date',
        )