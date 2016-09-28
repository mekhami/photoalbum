from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify


# Create your models here.
def photo_path(instance, filename):
    return 'user_{0}/{1}/{2}'.format(instance.uploader.id, instance.album.id, filename)


class Album(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_albums')
    slug = models.CharField(max_length=255)
    allowed_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='invited_albums')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}: {}".format(self.owner, self.name)

    def get_absolute_url(self):
        return reverse("album:album-detail", kwargs={'slug': self.slug})


class Photo(models.Model):
    album = models.ForeignKey(Album)
    date_created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to=photo_path)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return "{}: {}".format(self.uploader, self.photo.name)

    def get_absolute_url(self):
        return reverse("album:photo-detail", kwargs={'id': self.id, 'slug': self.album.slug})
