# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20150615_1102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='isDeleted',
            new_name='is_deleted',
        ),
    ]
