from django import template
from archive.models import *
import itertools

register = template.Library()

@register.simple_tag
def music_genres():
    return MusicGenre.objects.all()

@register.simple_tag
def artistsdict():
    artist_dict = {}
    artists = Artist.objects.filter(is_active=True).order_by('name_eng')
    key_l = lambda x : x.name_eng[0]
    for key, group in itertools.groupby(artists, key_l):
        artist_dict[key] = list(group)
    return artist_dict

@register.simple_tag
def artists():
    artists = Artist.objects.filter(is_active=True).order_by('name_eng')
    return artists

@register.simple_tag
def maqams():
    maqams = Maqam.objects.all().order_by('title_eng')
    return maqams

@register.simple_tag
def rythms():
    rythms = Rythm.objects.all().order_by('title_eng')
    return rythms

@register.simple_tag
def artist_types():
    return ArtistType.objects.all()

@register.simple_tag
def music_forms():
    return MusicForm.objects.all()

@register.simple_tag
def ft_artists():
    ft_artists = Artist.objects.filter(is_active=True).order_by('-created_at')[:2]
    return ft_artists

@register.simple_tag
def ft_songs():
    ft_songs = Song.objects.filter(is_active=True).order_by('-created_at')[:2]
    return ft_songs