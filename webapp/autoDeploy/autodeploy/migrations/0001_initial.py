# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.IntegerField(serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('repo', models.CharField(max_length=255, blank=True)),
                ('lastCommit', models.CharField(max_length=32)),
                ('lastCommitDate', models.DateTimeField()),
            ],
        ),
    ]
