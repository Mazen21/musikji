# Generated by Django 3.0.3 on 2020-07-04 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0006_auto_20200704_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='score_msc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='score_youtube',
            field=models.TextField(blank=True, null=True),
        ),
    ]
