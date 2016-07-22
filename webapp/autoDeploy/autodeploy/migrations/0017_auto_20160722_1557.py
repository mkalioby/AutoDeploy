# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0016_auto_20151101_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='last_seen',
            field=models.DateTimeField(default='2016-01-01 00:00:00', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 22, 15, 56, 42, 972519), blank=True),
        ),
    ]
