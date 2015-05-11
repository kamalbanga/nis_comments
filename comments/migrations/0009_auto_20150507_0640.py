# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0008_auto_20150505_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='author',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='text',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
