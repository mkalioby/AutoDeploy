# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0002_auto_20150508_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='configFile',
            field=models.FileField(upload_to=b'', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='repo_type',
            field=models.CharField(max_length=10, blank=True),
        ),
    ]
