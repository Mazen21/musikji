# Generated by Django 3.0.3 on 2020-08-04 12:09

import archive.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0010_auto_20200729_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='date',
            field=models.PositiveIntegerField(blank=True, default=2020, null=True, validators=[django.core.validators.MinValueValidator(500), archive.models.max_value_current_year]),
        ),
    ]
