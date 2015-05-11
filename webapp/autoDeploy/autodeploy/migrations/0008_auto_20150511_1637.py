# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0007_auto_20150510_1427'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='dns',
            new_name='ip',
        ),
        migrations.AddField(
            model_name='server',
            name='DNS',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 11, 16, 37, 3, 358918), blank=True),
        ),
    ]
