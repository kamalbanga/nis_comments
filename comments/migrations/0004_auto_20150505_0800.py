# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20150504_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('news_id', models.CharField(max_length=1000)),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.OneToOneField(primary_key=True, serialize=False, to='comments.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='news',
            field=models.ForeignKey(to='comments.News'),
            preserve_default=False,
        ),
    ]
