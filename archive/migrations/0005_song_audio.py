# Generated by Django 3.0.3 on 2020-07-04 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0004_song_music_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='audio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
