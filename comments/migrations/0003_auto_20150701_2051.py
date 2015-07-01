# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20150630_1318'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('news_id', 'user')]),
        ),
    ]
