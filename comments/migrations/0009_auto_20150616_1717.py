# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0008_allapproved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allapproved',
            name='news_id',
            field=models.CharField(max_length=200, unique=True, null=True),
        ),
    ]
