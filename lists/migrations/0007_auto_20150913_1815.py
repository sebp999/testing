# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0006_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([]),
        ),
    ]
