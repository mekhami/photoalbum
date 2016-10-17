from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Album, Photo
from .forms import PhotoForm


# Create your views here.
class AlbumList(LoginRequiredMixin, generic.ListView):
    model = Album

    def get_queryset(self):
        return Album.objects.filter(Q(owner=self.request.user) | Q())

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

    def get_object(self, queryset=None):
        album = get_object_or_404(Album, slug=self.kwargs.get('slug'))
        photo = get_object_or_404(Photo, album=album, id=self.kwargs.get('id'))
        return photo


class PhotoCreate(LoginRequiredMixin, generic.CreateView):
    model = Photo
    form_class = PhotoForm

    def get_object(self, queryset=None):
        album = get_object_or_404(Album, slug=self.kwargs.get('slug'))
        return album

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['album'] = self.get_object()
        return context

    def get_initial(self):
        return {
            'album': self.get_object(),
            'uploader': self.request.user,
        }
