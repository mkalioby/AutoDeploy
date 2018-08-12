# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autodeploy', '0015_auto_20171123_0937'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='deployment_server',
            name='deployed',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='project',
            name='autoDeploy',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 7, 16, 51, 46, 165178), blank=True),
        ),
        migrations.AddField(
            model_name='user_project',
            name='project',
            field=models.ForeignKey(to='autodeploy.Project'),
        ),
        migrations.AddField(
            model_name='user_project',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
