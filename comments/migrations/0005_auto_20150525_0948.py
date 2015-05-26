# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20150525_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=40),
        ),
    ]
