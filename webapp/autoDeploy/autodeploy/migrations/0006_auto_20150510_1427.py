# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0005_auto_20150509_0744'),
    ]

    operations = [
        migrations.CreateModel(
            name='working_directory',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('path', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='deployment_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='repo_link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastCommitDate',
            field=models.DateTimeField(default=b'1970-01-01', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 10, 14, 27, 1, 48900), blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='sshKey',
            field=models.ForeignKey(verbose_name=b'SSH Key', to='autodeploy.sshKey'),
        ),
    ]
