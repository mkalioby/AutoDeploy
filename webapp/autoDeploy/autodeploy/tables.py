import django_tables2 as tables
from django_tables2_reports.tables import TableReport
from models import *
__author__ = 'mohamed'


class ProjectReport(TableReport):
    name=tables.Column(verbose_name="Project Name")
    Operations=tables.TemplateColumn("<a href='./clone?project={{record.name}}'><span title='Clone' class='fa fa-download'></span></a>&nbsp;&nbsp;<a href='./deploy?project={{record.name}}'><span title='Deploy' class='fa fa-codepen'></span></a>")
    repo_link=tables.TemplateColumn("<a href='{{ record.repo_link }}' target='blank'>{{ record.repo_link }}</a> ")
    deployment_link=tables.TemplateColumn("<a href='{{ record.deployment_link }}' target='blank'>{{ record.deployment_link }}</a> ")
    class Meta:
        model=Project
        fields=('name','repo_link','deployment_link')
        attrs = {"class": "paleblue"}
