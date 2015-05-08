# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='lastTag',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 8, 19, 41, 23, 906454, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='working_dir',
            field=models.FileField(upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastCommit',
            field=models.CharField(max_length=32, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastCommitDate',
            field=models.DateTimeField(blank=True),
        ),
    ]
