# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0010_auto_20150519_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='update_style',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 19, 18, 11, 25, 191104), blank=True),
        ),
    ]
