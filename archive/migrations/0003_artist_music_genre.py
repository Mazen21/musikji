# Generated by Django 3.0.3 on 2020-06-13 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0002_musicgenre'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='music_genre',
            field=models.ManyToManyField(to='archive.MusicGenre'),
        ),
    ]
