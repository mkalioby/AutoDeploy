# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0004_auto_20150509_0522'),
    ]

    operations = [
        migrations.CreateModel(
            name='sshKey',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('key', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='sshKey',
            field=models.ForeignKey(default='NULL', to='autodeploy.sshKey'),
            preserve_default=False,
        ),
    ]
