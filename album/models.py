from django.db import models
from django.contrib.auth.models import User


# Create your models here.
def user_album_path(instance, album, filename):
    return 'user_{0}/{1}/{2}'.format(instance.user.id, instance.album.id, filename)


class Album(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User)


class Photo(models.Model):
    photo = models.ImageField(upload_to=user_album_path)
    album = models.ForeignKey(Album)
