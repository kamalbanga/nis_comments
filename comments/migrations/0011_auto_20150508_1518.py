# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0010_auto_20150507_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='downvote_table',
            field=models.ManyToManyField(related_name='downvote', null=True, to='comments.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='upvote_table',
            field=models.ManyToManyField(related_name='upvote', null=True, to='comments.User'),
        ),
    ]
