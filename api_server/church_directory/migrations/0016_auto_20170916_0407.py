# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 04:07
from __future__ import unicode_literals

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('church_directory', '0015_auto_20170822_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='address_line1',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Address Line 1'),
        ),
        migrations.AlterField(
            model_name='person',
            name='marital_status',
            field=models.IntegerField(choices=[(0, 'N/A'), (1, 'Single'), (2, 'Married')]),
        ),
        migrations.AlterField(
            model_name='person',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='notes'),
        ),
        migrations.AlterField(
            model_name='person',
            name='picture',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], keep_meta=True, null=True, quality=0, size=[360, 230], upload_to='images/church_directory/person/pictures'),
        ),
    ]