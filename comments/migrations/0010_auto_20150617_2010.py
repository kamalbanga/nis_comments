# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0009_auto_20150616_1717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='news_slug',
            new_name='news_id',
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('news_id', 'user')]),
        ),
    ]
