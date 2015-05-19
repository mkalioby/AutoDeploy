# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0011_auto_20150519_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='newVersion',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 19, 19, 43, 49, 254988), blank=True),
        ),
    ]
