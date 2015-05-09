# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0003_auto_20150508_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('dns', models.CharField(max_length=50)),
                ('port', models.IntegerField(default=4567)),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='id',
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
    ]
