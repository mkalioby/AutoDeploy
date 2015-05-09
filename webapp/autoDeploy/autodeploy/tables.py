import django_tables2 as tables
from django_tables2_reports.tables import TableReport
from models import *
__author__ = 'mohamed'


class ProjectReport(TableReport):
    name=tables.Column(verbose_name="Project Name")
    Operations=tables.TemplateColumn("<a href='./clone?project={{record.name}}'><span title='Clone' class='fa fa-download'></span></a>&nbsp;&nbsp;<a href='./deploy?project={{record.name}}'><span title='Deploy' class='fa fa-codepen'></span></a>")
    class Meta:
        model=Project
        fields=('name','repo')
        attrs = {"class": "paleblue"}
