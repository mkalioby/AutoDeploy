import django_tables2 as Table
import django_tables2.tables as tables
from django_tables2_reports.tables import TableReport
from models import *
__author__ = 'mohamed'


class ProjectReport(TableReport):
    name=Table.Column(verbose_name="Project Name")
    Operations=Table.TemplateColumn("<a href='{{BASE_URL}}clone?project={{record.name}}'><span title='Clone' class='fa fa-download'></span></a>&nbsp;&nbsp;<a href='./deploy?project={{record.name}}'><span title='Deploy' class='fa fa-codepen'></span></a>&nbsp;<a href='{{BASE_URL}}getDeploymentHistory?project={{record.name}}'><span class='fa fa-history' title='Deployment History'></span></a>")
    repo_link=Table.TemplateColumn("<a href='{{ record.repo_link }}' target='blank'>{{ record.repo_link }}</a> ")
    deployment_link=Table.TemplateColumn("<a href='{{ record.deployment_link }}' target='blank'>{{ record.deployment_link }}</a> ")

    class Meta:
        model=Project
        fields=('name','repo_link','deployment_link')
        attrs = {"class": "paleblue"}


class SSHKeysReport(TableReport):
    Operations=Table.TemplateColumn("<a href='edit_sshkey/{{record.name}}'><span class='fa fa-edit' title='Edit'></span></a>&nbsp;&nbsp;<a href='delete_sshkey/{{record.name}}'><span class='fa fa-trash' title='Delete'></span></a>")
    class Meta:
        model=SSHKey
        fields=("name","Operations")
        attrs = {"class": "paleblue"}

class CommitTable(Table.Table):
    Short=Table.TemplateColumn("<a href='../deploy3?commit={{record.Hash}}'>{{record.Short}}</a>",verbose_name="Hash")
    Author=Table.Column()
    Committed=Table.Column()
    Message=Table.Column()
    class Meta:
        attrs={"class": "paleblue"}
        fields=["Short","Author","Committed","Message"]
        sequence=["Short","Author","Committed","Message"]

class DeploymentHistory(TableReport):
    class Meta:
        model=Deployment_Server
        fields=["datetime","server","update_type","update_version","has_new_version"]
        sequence=["datetime","server","update_type","update_version","has_new_version"]
        attrs={"class": "paleblue"}