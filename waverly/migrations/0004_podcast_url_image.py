# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 06:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waverly', '0003_podcast_url_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='url_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
