from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from jsonfield import JSONField


class CIProject(models.Model):
    name = models.CharField(max_length=50, blank=False,primary_key=True)
    repo_type = models.CharField(max_length=10,blank=True)
    repo = models.CharField(max_length=255, blank=True)
    default_server = models.ForeignKey('deployment.Server',blank=True,on_delete=models.DO_NOTHING)
    update_style = models.CharField(max_length=10,blank=True)
    lastCommit = models.CharField(max_length=50,blank=True)
    lastTag = models.CharField(max_length=255,blank=True)
    lastCommitDate = models.DateTimeField(blank=True,default="1970-01-01")
    working_dir = models.FileField(blank=True)
    configFile = models.FileField(blank=True)
    lastUpdate = models.DateTimeField(blank=True, default=datetime.now())
    sshKey = models.ForeignKey('deployment.SSHKey',on_delete=models.DO_NOTHING)
    repo_link = models.URLField(blank=True)
    integration_link = models.CharField(max_length=200, blank=True)
    newVersion = models.BooleanField(default=False)
    emailUsers = models.TextField(default="", blank=True)
    autoDeploy = models.BooleanField(default=False)
    default_branch = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'Integration_Project'

    def status(self):
        last_ci = Integration_server.objects.filter(update_version=self.lastCommit).order_by('-id')
        return last_ci[0].status.description if last_ci.exists() else None

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class CIntegrationStatus(models.Model):
    code = models.IntegerField(db_column='Code', primary_key=True)
    description = models.CharField(db_column='Description', max_length=50, blank=True, unique=True)

    def __unicode__(self):
        return self.description

    def __str__(self):
        return self.description

    class Meta:
        app_label = 'integration'
        db_table = 'C_Integration_Status'
        ordering = ['code']

class Integration_server(models.Model):
    datetime = models.DateTimeField()
    update_type = models.CharField(max_length=6)
    update_version = models.CharField(max_length=255)
    has_new_version = models.IntegerField(verbose_name="Updates Behind")
    project = models.ForeignKey(CIProject,on_delete=models.DO_NOTHING)
    server = models.ForeignKey('deployment.Server',on_delete=models.DO_NOTHING)
    status = models.ForeignKey(CIntegrationStatus,on_delete=models.DO_NOTHING,default=0)
    result = JSONField(db_column="result",default="")

    class Meta:
        get_latest_by = "id"
        db_table = 'Integration_Server'


class CIUser_Project(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    project = models.ForeignKey(CIProject,on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return "%s -- %s" % (self.user.username, self.project_id)

    def __str__(self):
        return "%s -- %s" % (self.user.username, self.project_id)

    class Meta:
        verbose_name_plural = "Integration_Users_Projects"
        db_table = 'Integration_User_Project'
