# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0014_auto_20160514_1317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deployment_server',
            options={'get_latest_by': 'id'},
        ),
        # migrations.AddField(
        #     model_name='deployment_server',
        #     name='deployed',
        #     field=models.BooleanField(default=True),
        # ),
        # # migrations.AddField(
        #     model_name='project',
        #     name='autoDeploy',
        #     field=models.BooleanField(default=False),
        # ),
        migrations.AddField(
            model_name='project',
            name='default_branch',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 23, 9, 37, 18, 29660), blank=True),
        ),
    ]
