# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deployment_Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('update_type', models.CharField(max_length=6)),
                ('update_version', models.CharField(max_length=255)),
                ('has_new_version', models.IntegerField(verbose_name='Updates Behind')),
                ('deployed', models.BooleanField(default=True)),
            ],
            options={
                'get_latest_by': 'id',
                'verbose_name_plural': 'Deployment_Server',
                'db_table': 'Deployment_Server',
            },
        ),
        migrations.CreateModel(
            name='Plugins',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('settings', models.TextField()),
            ],
            options={
                'db_table': 'Plugins',
                'verbose_name_plural': 'Plugins',
            },
        ),
        migrations.CreateModel(
            name='Project',
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
                ('lastUpdate', models.DateTimeField(auto_now_add=True)),
                ('repo_link', models.URLField(blank=True)),
                ('deployment_link', models.CharField(max_length=200, blank=True)),
                ('newVersion', models.BooleanField(default=False)),
                ('emailUsers', models.TextField(default='', blank=True)),
                ('autoDeploy', models.BooleanField(default=False)),
                ('default_branch', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('ip', models.CharField(max_length=50)),
                ('port', models.IntegerField(default=4567)),
                ('DNS', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'db_table': 'Server',
            },
        ),
        migrations.CreateModel(
            name='SSHKey',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('key', models.TextField()),
            ],
            options={
                'db_table': 'SSHKey',
            },
        ),
        migrations.CreateModel(
            name='User_Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.ForeignKey(to='deployment.Project',on_delete=models.DO_NOTHING)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)),
            ],
            options={
                'db_table': 'User_Project',
                'verbose_name_plural': 'Users_Projects',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='default_server',
            field=models.ForeignKey(to='deployment.Server', blank=True,on_delete=models.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='project',
            name='sshKey',
            field=models.ForeignKey(verbose_name=b'SSH Key', to='deployment.SSHKey',on_delete=models.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='deployment_server',
            name='project',
            field=models.ForeignKey(to='deployment.Project',on_delete=models.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='deployment_server',
            name='server',
            field=models.ForeignKey(to='deployment.Server',on_delete=models.DO_NOTHING),
        ),
    ]
