from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class SSHKey(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    key = models.TextField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        db_table = "SSHKey"


class Server(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    ip = models.CharField(max_length=50)
    port = models.IntegerField(default=4567)
    DNS = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Server"


class Project(models.Model):
    name = models.CharField(max_length=50, blank=False, primary_key=True)
    repo_type = models.CharField(max_length=10, blank=True)
    repo = models.CharField(max_length=255, blank=True)
    default_server = models.ForeignKey(Server, blank=True,on_delete=models.DO_NOTHING)
    update_style = models.CharField(max_length=10, blank=True)
    lastCommit = models.CharField(max_length=50, blank=True)
    lastTag = models.CharField(max_length=255, blank=True)
    lastCommitDate = models.DateTimeField(blank=True, default="1970-01-01")
    working_dir = models.FileField(blank=True)
    configFile = models.FileField(blank=True)
    lastUpdate = models.DateTimeField(blank=True,auto_now_add=True)
    sshKey = models.ForeignKey(SSHKey, to_field="name", verbose_name="SSH Key",on_delete=models.DO_NOTHING)
    repo_link = models.URLField(blank=True)
    deployment_link = models.CharField(max_length=200, blank=True)
    newVersion = models.BooleanField(default=False)
    emailUsers = models.TextField(default="", blank=True)
    autoDeploy = models.BooleanField(default=False)
    default_branch = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Deployment_Server(models.Model):
    datetime = models.DateTimeField()
    update_type = models.CharField(max_length=6)
    update_version = models.CharField(max_length=255)
    has_new_version = models.IntegerField(verbose_name="Updates Behind")
    project = models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    server = models.ForeignKey(Server,on_delete=models.DO_NOTHING)
    deployed = models.BooleanField(default=True)

    class Meta:
        get_latest_by = "id"
        verbose_name_plural = "Deployment_Server"
        db_table = 'Deployment_Server'


class Plugins(models.Model):
    name = models.CharField(max_length=50)
    settings = models.TextField()

    class Meta:
        verbose_name_plural = "Plugins"
        db_table = 'Plugins'


class User_Project(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project,on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return "%s -- %s" % (self.user.username, self.project_id)

    def __str__(self):
        return "%s -- %s" % (self.user.username, self.project_id)

    class Meta:
        verbose_name_plural = "Users_Projects"
        db_table = "User_Project"
