# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0014_auto_20150512_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='downvote_table',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='upvote_table',
        ),
        migrations.AddField(
            model_name='vote',
            name='cmt',
            field=models.ForeignKey(to='comments.Comment'),
        ),
        migrations.AddField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='votes',
            field=models.ManyToManyField(related_name='votes_table', through='comments.Vote', to=settings.AUTH_USER_MODEL),
        ),
    ]
