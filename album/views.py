from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import generic

from .models import Album, Photo


# Create your views here.
class AlbumCreate(LoginRequiredMixin, generic.CreateView):
    model = Album
    fields = ['name', 'owner']

    def get_success_url(self):
        return self.object.get_absolute_url()


class AlbumDetail(LoginRequiredMixin, generic.DetailView):
    model = Album

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        if self.request.user in obj.allowed_users.all() or self.request.user == obj.owner:
            return obj
        raise PermissionDenied


class PhotoDetail(LoginRequiredMixin, generic.DetailView):
    model = Photo
