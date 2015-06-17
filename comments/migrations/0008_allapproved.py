# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0007_auto_20150616_0714'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllApproved',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('news_id', models.CharField(max_length=200, null=True)),
                ('all_approved', models.BooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
