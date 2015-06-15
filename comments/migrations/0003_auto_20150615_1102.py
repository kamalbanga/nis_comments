# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_emailuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailuser',
            name='facebook_id',
            field=models.CharField(max_length=40, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailuser',
            name='source',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
    ]
