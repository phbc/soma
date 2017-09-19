# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 04:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

from church_directory.models import EventType, LIFE_EVENTS

def setup_event_types(apps, schema_editor):
    for v in LIFE_EVENTS:
        EventType(name=v, builtin=True).save()

def delete_event_types(apps, schema_editor):
    for v in LIFE_EVENTS:
        EventType.objects.get(name=v).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('church_directory', '0009_auto_20170919_2234'), # required for setup_event_types
    ]

    operations = [
        migrations.RunPython(setup_event_types, delete_event_types),
    ]
