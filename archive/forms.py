from django import forms
from .models import Song, Lyric, Score, Artist, Comment
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_countries.widgets import CountrySelectWidget

class LyricForm(forms.ModelForm):

    class Meta:
        model = Lyric
        fields = ['song','writer','lyric']
        widgets = {
        'lyric': SummernoteWidget(),
    }

class ScoreForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ['song','note','score']

class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        labels = {
            "name_eng": "Name",
            "birth": "Date of birth",
            "death": "Date of death",
            "description_eng": "Description",
            "artist_type":"Type",
            "music_genre":"Music genre",
        }
        fields = ['image','name_eng','artist_type','music_genre','country','birth','death','description_eng']
        widgets = {
        'birth': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        'death': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        'country': CountrySelectWidget()
    }

class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        labels = {
            "name_eng":"Name",
            "artists":"Featured Artists",
            "maqam":"Maqam",
            "rythm":"Rythm",
            "music_form":"Music Form",
            "date":"Date",
        }
        fields = ['name_eng','artists','maqam','rythm','music_form','date']

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        labels = {
            "body":"",
        }
        fields = ('body',)
        widgets = {
        'body': SummernoteWidget(),
    }