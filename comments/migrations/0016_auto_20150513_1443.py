# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0015_auto_20150513_1322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='vote',
            new_name='vote_type',
        ),
    ]
