# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20150611_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailuser',
            name='image_url',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailuser',
            name='name',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
