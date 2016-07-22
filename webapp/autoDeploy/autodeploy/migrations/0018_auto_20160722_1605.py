# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0017_auto_20160722_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='lastCommit',
            field=models.CharField(max_length=45, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 22, 16, 5, 17, 13046), blank=True),
        ),
    ]
