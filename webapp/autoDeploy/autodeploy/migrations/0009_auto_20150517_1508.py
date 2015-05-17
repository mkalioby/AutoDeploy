# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0008_auto_20150511_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deployment_Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('update_type', models.CharField(max_length=6)),
                ('update_version', models.CharField(max_length=255)),
                ('has_new_version', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='deployment_link',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 17, 15, 8, 51, 406788), blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='sshKey',
            field=models.ForeignKey(verbose_name=b'SSH Key', to='autodeploy.SSHKey'),
        ),
        migrations.AddField(
            model_name='deployment_server',
            name='project',
            field=models.ForeignKey(to='autodeploy.Project'),
        ),
        migrations.AddField(
            model_name='deployment_server',
            name='server',
            field=models.ForeignKey(to='autodeploy.Server'),
        ),
    ]
