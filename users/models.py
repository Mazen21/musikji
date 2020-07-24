from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from archive.models import Score, Instrument, MusicGenre
from django_countries.fields import CountryField
from directmessages.apps import Inbox

class Badge(models.Model):
    css_class_eng = [
        ('primary','Blue'),
        ('secondary','Gray'),
        ('success','Green'),
        ('danger','Red'),
        ('warning','Yello'),
        ('info','Turquoise'),
        ('light','light grey'),
        ('dark','Black'),
    ]
    title_eng = models.CharField(max_length=50)
    css_class = models.CharField(choices=css_class_eng, max_length=50, default='string')

    def __str__(self):
        return self.title_eng

class Profile(models.Model):
    roles = [
        ('admin','admin'),
        ('moderator','moderator'),
        ('normal_user','normal_user'),
    ]

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150,blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    birthday = models.DateField(blank=True, null=True)
    points = models.IntegerField(default= 500 )
    website = models.URLField(max_length=200, blank=True)
    about = models.CharField(max_length=250, blank=True)
    image = models.ImageField(default='default.jpg', upload_to="profile_pics")
    favorit_scores = models.ManyToManyField(Score, blank=True)
    instruments = models.ManyToManyField(Instrument, blank=True)
    badges = models.ManyToManyField(Badge, blank=True)
    experience = models.TextField(blank=True)
    city = models.CharField(max_length=250, blank=True)
    country = CountryField(blank=True)
    role = models.CharField(choices=roles,max_length=50,blank=True,null=True,default='normal_user')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300 :
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Band(models.Model):
    name_eng = models.CharField(max_length=25)
    image = models.ImageField(default='default_band.jpg', upload_to="band_pics")
    musicians = models.ManyToManyField(Profile)

    def __str__(self):
        return self.name_eng
