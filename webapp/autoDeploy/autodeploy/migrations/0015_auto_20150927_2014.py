# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0014_auto_20150927_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment_server',
            name='deployed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 27, 20, 14, 51, 519592), blank=True),
        ),
    ]
