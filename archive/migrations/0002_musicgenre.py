# Generated by Django 3.0.3 on 2020-06-13 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_eng', models.CharField(max_length=100)),
                ('description_eng', models.TextField(blank=True)),
            ],
        ),
    ]
