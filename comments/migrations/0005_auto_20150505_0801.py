# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20150505_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='news_id',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
