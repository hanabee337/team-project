from django.db import models


class Music(models.Model):
    id_num = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    artist = models.TextField(max_length=255)
    preview = models.TextField(max_length=500)

    artist_picture_small = models.TextField(max_length=500)
    artist_picture_medium = models.TextField(max_length=500)
    artist_picture_big = models.TextField(max_length=500)

    album_picture_small = models.TextField(max_length=500)
    album_picture_medium = models.TextField(max_length=500)
    album_picture_big = models.TextField(max_length=500)




    def __str__(self):
        return self.title
