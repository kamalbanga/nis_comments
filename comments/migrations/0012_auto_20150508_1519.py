# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0011_auto_20150508_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='downvote_table',
            field=models.ManyToManyField(related_name='downvote', to='comments.User'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='upvote_table',
            field=models.ManyToManyField(related_name='upvote', to='comments.User'),
        ),
    ]
