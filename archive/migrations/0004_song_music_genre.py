# Generated by Django 3.0.3 on 2020-06-13 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0003_artist_music_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='music_genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive.MusicGenre'),
        ),
    ]