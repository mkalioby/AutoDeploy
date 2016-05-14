# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0013_auto_20150817_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='lastCommit',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 14, 13, 17, 34, 809478), blank=True),
        ),
    ]
