from django.db import models


class Project(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, blank=False)
    repo = models.CharField(max_length=255, blank=True)
    lastCommit = models.CharField(max_length=32)
    lastCommitDate = models.DateTimeField()