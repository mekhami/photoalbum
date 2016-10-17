from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create/$', views.AlbumCreate.as_view(), name='album-create'),
    url(r'^(?P<slug>[\w-]+)/$', views.AlbumDetail.as_view(), name='album-detail'),
    url(r'^(?P<slug>[\w-]+)/photo/upload/$', views.PhotoCreate.as_view(), name='photo-create'),
    url(r'^(?P<slug>[\w-]+)/photo/(?P<id>[\w]+)/$', views.PhotoDetail.as_view(), name='photo-detail'),
]
