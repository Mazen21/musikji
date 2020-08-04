# Generated by Django 3.0.3 on 2020-08-04 12:13

import archive.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0011_auto_20200804_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='date',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[archive.models.max_value_current_year]),
        ),
    ]
