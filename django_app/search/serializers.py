from rest_framework import serializers
from search.models import Music


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('artist', 'title', 'preview', 'artist_picture', 'album_picture')



# class MusicSerializer(serializers.Serializer):
#     artist = serializers.CharField(max_length=255, default='')
#     title = serializers.CharField(max_length=255)
#     preview = serializers.CharField(max_length=500, default='')
#     artist_picture = serializers.CharField(max_length=500)
#     album_picture = serializers.CharField(max_length=500)
#
#     def create(self, validated_data):
#         return Music.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.artist = validated_data.get('artist', instance.artist)
#         instance.title = validated_data.get('title', instance.title)
#         instance.preview = validated_data.get('preview', instance.preview)
#         instance.artist_picture = validated_data.get('artist_picture', instance.artist_picture)
#         instance.album_picture = validated_data.get('album_picture', instance.album_picture)
#         instance.save()
#         return instance
