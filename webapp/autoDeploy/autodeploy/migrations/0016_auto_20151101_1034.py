# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0015_auto_20150927_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='autoDeploy',
            field=models.BooleanField(default=False, verbose_name=b'Deploy new changes automatically?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 10, 34, 35, 620141), blank=True),
        ),
    ]
