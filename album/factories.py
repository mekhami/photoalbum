import os

import factory

from .models import Photo, Album


TEST_IMAGE = os.path.join(os.path.dirname(__file__), 'tests/files/potato.jpg')


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    album = factory.SubFactory('album.factories.AlbumFactory')
    photo = factory.django.ImageField(from_path=TEST_IMAGE, filename='potato.jpg')
    uploader = factory.SubFactory('photoalbums.users.tests.factories.UserFactory')


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album

    name = factory.Faker('sentence').generate({'nb_words': 4})
    owner = factory.SubFactory('photoalbums.users.tests.factories.UserFactory')
