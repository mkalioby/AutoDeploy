# -*- coding: utf-8 -*-


from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0003_migrate_data_from_old_to_new'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CIProject',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('repo_type', models.CharField(max_length=10, blank=True)),
                ('repo', models.CharField(max_length=255, blank=True)),
                ('update_style', models.CharField(max_length=10, blank=True)),
                ('lastCommit', models.CharField(max_length=50, blank=True)),
                ('lastTag', models.CharField(max_length=255, blank=True)),
                ('lastCommitDate', models.DateTimeField(default='1970-01-01', blank=True)),
                ('working_dir', models.FileField(upload_to='', blank=True)),
                ('configFile', models.FileField(upload_to='', blank=True)),
                ('lastUpdate', models.DateTimeField(default=datetime.datetime(2020, 9, 22, 12, 36, 50, 757401), blank=True)),
                ('repo_link', models.URLField(blank=True)),
                ('integration_link', models.CharField(max_length=200, blank=True)),
                ('newVersion', models.BooleanField(default=False)),
                ('emailUsers', models.TextField(default='', blank=True)),
                ('autoDeploy', models.BooleanField(default=False)),
                ('default_branch', models.CharField(max_length=255, null=True)),
                ('default_server', models.ForeignKey(to='deployment.Server', blank=True,on_delete=models.DO_NOTHING)),
                ('sshKey', models.ForeignKey(to='deployment.SSHKey',on_delete=models.DO_NOTHING)),
            ],
            options={
                'db_table': 'Integration_Project',
            },
        ),
        migrations.CreateModel(
            name='CIUser_Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.ForeignKey(to='integration.CIProject',on_delete=models.DO_NOTHING)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)),
            ],
            options={
                'db_table': 'Integration_User_Project',
                'verbose_name_plural': 'Integration_Users_Projects',
            },
        ),
        migrations.CreateModel(
            name='Integration_server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('update_type', models.CharField(max_length=6)),
                ('update_version', models.CharField(max_length=255)),
                ('has_new_version', models.IntegerField(verbose_name=b'Updates Behind')),
                ('deployed', models.BooleanField(default=True)),
                ('project', models.ForeignKey(to='integration.CIProject',on_delete=models.DO_NOTHING)),
                ('server', models.ForeignKey(to='deployment.Server',on_delete=models.DO_NOTHING)),
            ],
            options={
                'db_table': 'Integration_Server',
                'get_latest_by': 'id',
            },
        ),
    ]
