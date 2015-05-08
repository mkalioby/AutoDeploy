from django.db import models


class Project(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, blank=False)
    repo_type=models.CharField(max_length=10,blank=True)
    repo = models.CharField(max_length=255, blank=True)
    lastCommit = models.CharField(max_length=32,blank=True)
    lastTag=models.CharField(max_length=255,blank=True)
    lastCommitDate = models.DateTimeField(blank=True)
    working_dir=models.FileField(blank=True)
    configFile=models.FileField(blank=True)
    lastUpdate=models.DateTimeField(blank=True)