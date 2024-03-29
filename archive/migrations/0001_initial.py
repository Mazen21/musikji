# Generated by Django 3.0.3 on 2020-06-13 22:56

import archive.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(choices=[('youtube', 'youtube'), ('spotify', 'spotify')], max_length=25)),
                ('url', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('upvotes', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('downvotes', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('rank', models.IntegerField(blank=True, default=0, null=True)),
                ('rate', models.IntegerField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name_eng', models.CharField(max_length=150)),
                ('birth', models.DateField()),
                ('death', models.DateField(blank=True, null=True)),
                ('description_eng', models.CharField(max_length=800)),
                ('image', models.ImageField(upload_to='artists')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArtistType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_eng', models.CharField(max_length=100)),
                ('description_eng', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_eng', models.CharField(max_length=100)),
                ('description_eng', models.TextField(blank=True)),
                ('instrument_type_eng', models.CharField(choices=[('blow', 'blow'), ('string', 'string'), ('percussion', 'percussion')], default='string', max_length=100)),
                ('image', models.ImageField(upload_to='instruments/')),
                ('sound', models.FileField(blank=True, upload_to='instruments/')),
            ],
        ),
        migrations.CreateModel(
            name='Jins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_eng', models.CharField(max_length=100)),
                ('description_eng', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='jinss')),
                ('sound', models.FileField(upload_to='jinss')),
            ],
        ),
        migrations.CreateModel(
            name='Maqam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_eng', models.CharField(max_length=100)),
                ('description_eng', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='maqams/')),
                ('sound', models.FileField(blank=True, upload_to='maqams/')),
            ],
        ),
        migrations.CreateModel(
            name='MusicForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_eng', models.CharField(max_length=100)),
                ('description_eng', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rythm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_eng', models.CharField(max_length=100)),
                ('description_eng', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='rythms')),
                ('sound', models.FileField(upload_to='rythms')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('upvotes', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('downvotes', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('rank', models.IntegerField(blank=True, default=0, null=True)),
                ('rate', models.IntegerField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name_eng', models.CharField(max_length=150)),
                ('date', models.PositiveIntegerField(default=2020, validators=[django.core.validators.MinValueValidator(500), archive.models.max_value_current_year])),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('artists', models.ManyToManyField(to='archive.Artist')),
                ('maqam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive.Maqam')),
                ('music_form', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive.MusicForm')),
                ('rythm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive.Rythm')),
                ('votes', models.ManyToManyField(blank=True, to='archive.Vote')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('upvotes', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('downvotes', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('rank', models.IntegerField(blank=True, default=0, null=True)),
                ('rate', models.IntegerField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('note', models.CharField(blank=True, max_length=250)),
                ('score', models.FileField(upload_to=archive.models._score_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), archive.models.validate_size])),
                ('downloads', models.PositiveIntegerField(default=0)),
                ('front_image', models.ImageField(blank=True, null=True, upload_to='score_front_images/')),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.Song')),
                ('votes', models.ManyToManyField(blank=True, to='archive.Vote')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lyric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('upvotes', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('downvotes', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('rank', models.IntegerField(blank=True, default=0, null=True)),
                ('rate', models.IntegerField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('lyric', models.TextField()),
                ('note', models.CharField(blank=True, max_length=250)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.Song')),
                ('votes', models.ManyToManyField(blank=True, to='archive.Vote')),
                ('writer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive.Artist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('upvotes', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('downvotes', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('rank', models.IntegerField(blank=True, default=0, null=True)),
                ('rate', models.IntegerField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('body', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='archive.Song')),
                ('votes', models.ManyToManyField(blank=True, to='archive.Vote')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='artist',
            name='artist_type',
            field=models.ManyToManyField(to='archive.ArtistType'),
        ),
        migrations.AddField(
            model_name='artist',
            name='votes',
            field=models.ManyToManyField(blank=True, to='archive.Vote'),
        ),
    ]
