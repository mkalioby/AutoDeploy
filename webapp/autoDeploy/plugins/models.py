from django.db import models
from jsonfield import JSONField
from datetime import datetime


class Plugins(models.Model):
    name = models.CharField(max_length=100)
    settings = JSONField(db_column="settings", default={})
    created_on = models.DateTimeField(blank=True, default=datetime.now())


    class Meta:
        get_latest_by = "id"
        db_table = 'Plugins'
