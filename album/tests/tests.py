import tempfile

from django.test import TestCase

from .models import Photo


# Create your tests here.
class PhotoTests(TestCase):
    def setUp(self):
        self.photo = Photo()

    def test_absolute_url(self):
        self.assertEqual()
