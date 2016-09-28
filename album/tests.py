from django.test import TestCase, Client

from photoalbums.users.tests.factories import UserFactory
from . import factories
from . import views


# Create your tests here.
class PhotoTests(TestCase):
    def setUp(self):
        self.photo = factories.PhotoFactory()

    def test_absolute_url(self):
        self.photo.get_absolute_url()


class AlbumTests(TestCase):
    def setUp(self):
        self.owner = UserFactory()
        self.invited = UserFactory()
        self.album = factories.AlbumFactory(owner=self.owner)
        self.album.allowed_users.add(self.invited)
        self.album.save()
        self.client = Client()

    def test_absolute_url(self):
        self.album.get_absolute_url()

    def test_create_view_success_url(self):
        class_instance = views.AlbumCreate()
        setattr(class_instance, 'object', self.album)
        self.assertEqual(class_instance.get_success_url(), self.album.get_absolute_url())

    def test_anon_user_cannot_view_album(self):
        self.client.post('/accounts/logout')
        response = self.client.get(self.album.get_absolute_url())
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_cannot_view_album_unless_invited_or_owner(self):
        random_user = UserFactory()
        self.client.post(
            '/accounts/login/',
            {'login': random_user.email, 'password': 'password'}
        )
        response = self.client.get(self.album.get_absolute_url(), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_invited_user_can_view_album(self):
        self.client.post(
            '/accounts/login/',
            {'login': self.invited.email, 'password': 'password'}
        )
        response = self.client.get(self.album.get_absolute_url(), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_owner_can_view_album(self):
        self.client.post(
            '/accounts/login/',
            {'login': self.owner.email, 'password': 'password'}
        )
        response = self.client.get(self.album.get_absolute_url(), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_album_create_get(self):
        random_user = UserFactory()
        self.client.post(
            '/accounts/login/',
            {'login': random_user.email, 'password': 'password'}
        )
        response = self.client.get(
            '/albums/create/',
        )
        self.assertEqual(response.status_code, 200)

    def test_album_create_post(self):
        random_user = UserFactory()
        self.client.post(
            '/accounts/login/',
            {'login': random_user.email, 'password': 'password'}
        )
        response = self.client.post(
            '/albums/create/',
            {'name': 'Vacation 2016', 'owner': random_user.id},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
