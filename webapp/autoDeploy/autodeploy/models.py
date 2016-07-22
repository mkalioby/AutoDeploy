from django.db import models
from datetime import  datetime
class SSHKey(models.Model):
    name=models.CharField(max_length=50,primary_key=True)
    key=models.TextField()

    def __unicode__(self):
        return self.name


class working_directory(models.Model):
    name=models.CharField(max_length=50,primary_key=True)
    path=models.CharField(max_length=1000)

def __unicode__(self):
        return self.name

class Server(models.Model):
    name=models.CharField(max_length=50,primary_key=True)
    ip=models.CharField(max_length=50)
    port=models.IntegerField(default=4567)
    DNS=models.CharField(max_length=50,blank=True)
    behindFirewall=models.BooleanField(default=False)
    token=models.CharField(max_length=32,default=None,blank=True)
    last_seen=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=50, blank=False,primary_key=True)
    repo_type=models.CharField(max_length=10,blank=True)
    repo = models.CharField(max_length=255, blank=True)
    default_server=models.ForeignKey(Server,blank=True)
    update_style=models.CharField(max_length=10,blank=True)
    lastCommit = models.CharField(max_length=50,blank=True)
    lastTag=models.CharField(max_length=255,blank=True)
    lastCommitDate = models.DateTimeField(blank=True,default="1970-01-01")
    working_dir=models.FileField(blank=True)
    configFile=models.FileField(blank=True)
    lastUpdate=models.DateTimeField(blank=True,default=datetime.now())
    sshKey=models.ForeignKey(SSHKey,to_field="name",verbose_name="SSH Key")
    repo_link=models.URLField(blank=True)
    deployment_link=models.CharField(max_length=200,blank=True)
    newVersion=models.BooleanField(default=False)
    emailUsers=models.TextField(default="",blank=True)
    autoDeploy=models.BooleanField(default=False,verbose_name="Deploy new changes automatically?")

    def __unicode__(self):
        return self.name



class Deployment_Server(models.Model):
    datetime = models.DateTimeField()
    update_type = models.CharField(max_length=6)
    update_version = models.CharField(max_length=255)
    has_new_version = models.IntegerField(verbose_name="Updates Behind")
    project = models.ForeignKey(Project)
    server = models.ForeignKey(Server)
    deployed=models.BooleanField(default=False)

class Plugins(models.Model):
    name=models.CharField(max_length=50)
    settings=models.TextField()



