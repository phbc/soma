# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 03:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_directory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='cell_number',
            field=models.CharField(default=5555555555, max_length=10, verbose_name='Cell Number'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='home_number',
            field=models.CharField(default='5555555555', max_length=10, verbose_name='Home Number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='membership_status',
            field=models.IntegerField(choices=[(0, 'Non-member'), (1, 'Member'), (2, 'Member'), (3, 'Out-of-area Member'), (4, 'Former Member')]),
        ),
    ]
