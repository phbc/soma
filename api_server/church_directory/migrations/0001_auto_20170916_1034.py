# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-16 10:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_directory', '0019_event_event_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtype',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name=b'Name'),
        ),
    ]
