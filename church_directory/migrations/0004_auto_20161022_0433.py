# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 04:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_directory', '0003_auto_20161022_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/church_directory/person/pictures'),
        ),
    ]
