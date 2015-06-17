# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_auto_20150616_0706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='is_approved',
            field=models.NullBooleanField(),
        ),
    ]
