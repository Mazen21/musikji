from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator,MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from functools import partial
from django_countries.fields import CountryField
import hashlib
import datetime
import os
import logging

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

def validate_size(score):
    file_size = score.file.size
    if file_size >(2000 * 1024):
        raise ValidationError("Max file size reached ")
    else:
        return score    

def hash_file(file, block_size=65536):
    hasher = hashlib.sha256()
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)
    return hasher.hexdigest()

def _score_path(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return "score/{0}.{1}".format(hash_file(instance.score), filename_ext)

class MusicGenre(models.Model):
    title_eng = models.CharField(max_length=100)
    description_eng = models.TextField(blank=True)

    def __str__(self):
        return self.title_eng

class Vote(models.Model):
    value = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)

class MusikjiStamp(models.Model):
    name_orig = models.CharField(max_length=100,default='',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True)
    upvotes= models.PositiveSmallIntegerField(default=0,blank=True,null=True)
    downvotes= models.PositiveSmallIntegerField(default=0,blank=True,null=True)
    rank = models.IntegerField(default=0,blank=True,null=True)
    rate = models.IntegerField(default=0,blank=True,null=True)
    votes = models.ManyToManyField(Vote,blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class ArchiveLink(models.Model):
    tag_types = [
        ('youtube','youtube'),
        ('spotify','spotify'),
    ]
    tag = models.CharField(choices=tag_types, max_length=25)
    url = models.CharField(max_length=1000)

    def __str__(self):
        return tag

class Instrument(models.Model):
    instrument_types_eng = [
        ('blow','blow'),
        ('string','string'),
        ('percussion','percussion'),
    ]
    title_eng = models.CharField(max_length=100)
    description_eng = models.TextField(blank=True)
    instrument_type_eng = models.CharField(choices=instrument_types_eng, max_length=100, default='string')
    image = models.ImageField(upload_to='instruments/')
    audio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title_eng

class Maqam(models.Model):
    title_eng = models.CharField(max_length=100)
    description_eng = models.TextField(blank=True)
    image = models.ImageField(upload_to='maqams/')
    audio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title_eng

class Rythm(models.Model):
    title_eng = models.CharField(max_length=100)
    description_eng = models.TextField(blank=True)
    image = models.ImageField(upload_to='rythms')
    audio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title_eng

class Jins(models.Model):
    title_eng = models.CharField(max_length=100)
    description_eng = models.TextField(blank=True)
    image = models.ImageField(upload_to='jinss')
    audio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title_eng

class MusicForm(models.Model):
    title_eng = models.CharField(max_length=100)
    description_eng = models.TextField(blank=True)

    def __str__(self):
        return self.title_eng

class ArtistType(models.Model):
    title_eng = models.CharField(max_length=100)
    description_eng = models.TextField(blank=True)

    def __str__(self):
        return self.title_eng

class Artist(MusikjiStamp):
    name_eng = models.CharField(max_length=150)
    birth = models.DateField()
    death = models.DateField(blank=True, null=True)
    description_eng = models.CharField(max_length=800)
    image = models.ImageField(upload_to='artists')
    artist_type = models.ManyToManyField(ArtistType)
    music_genre = models.ManyToManyField(MusicGenre)
    country = CountryField(blank_label='(select country)', blank=True)

    def __str__(self):
        return self.name_eng
    
    def save(self, *args, **kwargs):
        self.name_eng = self.name_eng.title()
        return super(Artist, self).save(*args, **kwargs)

class Song(MusikjiStamp):
    name_eng = models.CharField(max_length=150)
    artists = models.ManyToManyField(Artist)
    maqam = models.ForeignKey(Maqam, on_delete=models.SET_NULL,null=True,blank=True)
    music_form = models.ForeignKey(MusicForm, on_delete=models.SET_NULL,null=True,blank=True)
    rythm = models.ForeignKey(Rythm,on_delete=models.SET_NULL, null=True,blank=True)
    music_genre = models.ForeignKey(MusicGenre,on_delete=models.SET_NULL, null=True,blank=True)
    date = models.PositiveIntegerField( validators=[max_value_current_year], null=True,blank=True)
    audio = models.TextField(null=True,blank=True)
    msc = models.TextField(blank=True, null=True)
    ytb = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name_eng

class Lyric(MusikjiStamp):
    song = models.ForeignKey(Song,on_delete=models.CASCADE)
    writer = models.ForeignKey(Artist,on_delete=models.SET_NULL, null=True,blank=True)
    lyric = models.TextField()
    note = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.song.name_eng + self.note

class Score(MusikjiStamp):
    song = models.ForeignKey(Song,on_delete=models.CASCADE)
    note = models.CharField(max_length=250, blank=True)
    score = models.FileField(upload_to=_score_path, 
        validators=[FileExtensionValidator(allowed_extensions=['pdf']), validate_size])
    downloads = models.PositiveIntegerField(default=0)
    front_image = models.ImageField(upload_to="score_front_images/",blank=True,null=True)

    def __str__(self):
        return self.song.name_eng + self.note 

class Comment(MusikjiStamp):
    post = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']