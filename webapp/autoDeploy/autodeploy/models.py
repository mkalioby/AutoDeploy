from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=50, blank=False,primary_key=True)
    repo_type=models.CharField(max_length=10,blank=True)
    repo = models.CharField(max_length=255, blank=True)
    lastCommit = models.CharField(max_length=32,blank=True)
    lastTag=models.CharField(max_length=255,blank=True)
    lastCommitDate = models.DateTimeField(blank=True)
    working_dir=models.FileField(blank=True)
    configFile=models.FileField(blank=True)
    lastUpdate=models.DateTimeField(blank=True)

class Server(models.Model):
    name=models.CharField(max_length=50,primary_key=True)
    dns=models.CharField(max_length=50)
    port=models.IntegerField(default=4567)

