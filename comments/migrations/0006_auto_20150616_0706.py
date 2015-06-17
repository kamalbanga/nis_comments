# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_comment_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='is_approved',
            field=models.BooleanField(),
        ),
    ]
