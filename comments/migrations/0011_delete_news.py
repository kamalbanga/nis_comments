# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0010_auto_20150617_2010'),
    ]

    operations = [
        migrations.DeleteModel(
            name='News',
        ),
    ]
