# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 04:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_directory', '0018_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='church_directory.EventType'),
            preserve_default=False,
        ),
    ]
