import django_tables2 as Table
import django_tables2.tables as tables
from django_tables2_reports.tables import TableReport
from django_tables2.export.views import ExportMixin
from .models import *
__author__ = 'mohamed'


class ProjectReport(ExportMixin, tables.Table):
    depLink="""
    {% if not "http" in record.deployment_link%}
        <a href='http://{{record.default_server.DNS}}{{ record.deployment_link }}' target='blank'>http://{{record.default_server.DNS}}{{ record.deployment_link }}</a>
    {% else %}
    <a href='{{ record.deployment_link }}' target='blank'>{{ record.deployment_link }}</a>
    {% endif %}
    """
    name=Table.Column(verbose_name="Project Name")
    Operations=Table.TemplateColumn("""
    {% if  perms.autodeploy.clone_project %}<a href='{{BASE_URL}}clone?project={{record.name}}'><span title='Clone' class='fa fa-download'></span></a>&nbsp;&nbsp;{%endif%}
    {% if  perms.autodeploy.deploy_project %}<a href='./deploy?project={{record.name}}'><span title='Deploy' class='fa fa-codepen'></span></a>&nbsp;{% endif %}
    <a href='{{BASE_URL}}getDeploymentHistory?project={{record.name}}'><span class='fa fa-history' title='Deployment History'></span></a>
    {% if  perms.autodeploy.change_project %}<a href='edit_project/{{record.name}}'>&nbsp;<span class='fa fa-edit' title='Edit'></span></a>&nbsp;&nbsp;{%endif%}
    {% if  perms.autodeploy.delete_project %}<a href='delete_project/{{record.name}}'><span class='fa fa-trash' title='Delete'></span></a>{%endif%}""")
    repo_link=Table.TemplateColumn("<a href='{{ record.repo_link }}' target='blank'>{{ record.repo_link }}</a> ",verbose_name="Source Link")
    deployment_link=Table.TemplateColumn(depLink,verbose_name="Deployment Link")
    #newVersion=Table.BooleanColumn(yesno="Yes,No",verbose_name=" Updates Avaliable")
    lastUpdate=Table.Column(verbose_name="Last Update")
    class Meta:
        model=Project
        fields=('name','repo_link','lastUpdate','deployment_link')
        attrs = {"class": "table table-striped"}




class SSHKeysReport(ExportMixin, tables.Table):
    Operations=Table.TemplateColumn("<a href='edit_sshkey/{{record.name}}'><span class='fa fa-edit' title='Edit'></span></a>&nbsp;&nbsp;<a href='delete_sshkey/{{record.name}}'><span class='fa fa-trash' title='Delete'></span></a>")
    class Meta:
        model=SSHKey
        fields=("name","Operations")
        attrs = {"class": "table table-striped"}

class ServersReport(ExportMixin, tables.Table):
    Operations=Table.TemplateColumn("<a href='edit_server/{{record.name}}'><span class='fa fa-edit' title='Edit'></span></a>&nbsp;&nbsp;<a href='delete_server/{{record.name}}'><span class='fa fa-trash' title='Delete'></span></a>")
    class Meta:
        model=SSHKey
        fields=("name","Operations")
        attrs = {"class": "table table-striped"}

class CommitTable(Table.Table):
    Short=Table.TemplateColumn("<a href='../deploy3?commit={{record.Hash}}'>{{record.Short}}</a>",verbose_name="Hash")
    Author=Table.Column()
    Committed=Table.Column()
    Message=Table.Column()
    class Meta:
        attrs={"class": "table table-striped"}
        fields=["Short","Author","Committed","Message"]
        sequence=["Short","Author","Committed","Message"]

class TagTable(Table.Table):
    ID=Table.TemplateColumn("<a href='../deploy3?tag={{record.Tag}}'>{{record.Tag}}</a>",verbose_name="Tag")
    Tagger=Table.Column()
    Date=Table.Column()
    Commit=Table.Column()
    class Meta:
        attrs={"class": "table table-striped"}
        fields=["ID","Tagger","Date","Commit"]
        sequence=["ID","Tagger","Date","Commit"]

class DeploymentHistory(ExportMixin, tables.Table):
    class Meta:
        model=Deployment_Server
        fields=["datetime","server","update_type","update_version","has_new_version"]
        sequence=["datetime","server","update_type","update_version","has_new_version"]
        attrs={"class": "table table-striped"}