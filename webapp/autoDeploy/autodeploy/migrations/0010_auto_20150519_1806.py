# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0009_auto_20150517_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='default_server',
            field=models.ForeignKey(default='localhost', blank=True, to='autodeploy.Server'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deployment_server',
            name='datetime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='deployment_server',
            name='has_new_version',
            field=models.IntegerField(verbose_name=b'Updates Behind'),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 19, 18, 5, 58, 418921), blank=True),
        ),
    ]
