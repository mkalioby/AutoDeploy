# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0013_auto_20150817_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='behindFirewall',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='server',
            name='token',
            field=models.CharField(default=None, max_length=32, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 27, 14, 56, 3, 4856), blank=True),
        ),
    ]
