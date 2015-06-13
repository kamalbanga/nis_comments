# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailuser',
            name='username',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
