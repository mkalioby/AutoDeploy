# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0012_auto_20150519_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plugins',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('settings', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='emailUsers',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 17, 12, 50, 51, 949082), blank=True),
        ),
    ]
