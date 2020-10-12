import django_tables2 as Table
import django_tables2.tables as tables
from django_tables2_reports.tables import TableReport
from django_tables2.export.views import ExportMixin
from django_tables2.utils import A
from .models import *
__author__ = 'mohamed'

class CIProjectReport(ExportMixin, tables.Table):
    name = Table.TemplateColumn("""<a style='text-decoration: none;color:inherit;' href='javascript:void(0)' onclick='getHistory(this,"{{record.lastCommit}}")' >{{ record.name }} - {{ record.default_branch}}</a>""",
        verbose_name="Project Name")
    Operations = Table.TemplateColumn("""
    {% if  perms.CI.clone_project %}<a href="{% url 'cloneci' %}?project={{record.name}}"><span title='Clone' class='fa fa-download'></span></a>&nbsp;&nbsp;{%endif%}
    {% if  perms.CI.integrate_project %}<a href="{% url 'integrate' %}?project={{record.name}}"><span title='Integrate' class='fa fa-codepen'></span></a>&nbsp;{% endif %}
    <a href="{% url 'getIntegrationHistory' %}?project={{record.name}}"><span class='fa fa-history' title='Integration History'></span></a>
    {% if  perms.CI.change_project %}<a href="{% url 'edit_ciproject' record.name %}">&nbsp;<span class='fa fa-edit' title='Edit'></span></a>&nbsp;&nbsp;{%endif%}
    {% if  perms.CI.delete_ci_project %}<a href="{% url 'delete_ciproject' record.name %}"><span class='fa fa-trash' title='Delete'></span></a>{%endif%}""")
    repo_link = Table.TemplateColumn("<a href='{{ record.repo_link }}' target='blank'>{{ record.repo_link }}</a> ",verbose_name="Source Link")
    lastUpdate = Table.Column(verbose_name="Last CI")
    status = Table.TemplateColumn("""{{ record.status }}""",verbose_name="Status")
    class Meta:
        model = CIProject
        fields = ('name', 'repo_link', 'lastUpdate')
        sequence = ('name', 'repo_link', 'lastUpdate','status', 'Operations')
        attrs = {"class": "table table-striped"}


class CommitTable(Table.Table):
    Short = Table.TemplateColumn("<a href='{% url 'integrate3' %}?commit={{record.Hash}}'>{{record.Short}}</a>",verbose_name="Hash")
    Author = Table.Column()
    Committed = Table.Column()
    Message = Table.Column()

    class Meta:
        attrs = {"class": "table table-striped"}
        fields = ["Short","Author","Committed","Message"]
        sequence = ["Short","Author","Committed","Message"]


class TagTable(Table.Table):
    ID = Table.TemplateColumn("<a href='{% url 'integrate3' %}?tag={{record.Tag}}'>{{record.Tag}}</a>",verbose_name="Tag")
    Tagger = Table.Column()
    Date = Table.Column()
    Commit = Table.Column()

    class Meta:
        attrs = {"class": "table table-striped"}
        fields = ["ID", "Tagger", "Date", "Commit"]
        sequence = ["ID", "Tagger", "Date", "Commit"]

class IntegrationHistory(ExportMixin, tables.Table):
    class Meta:
        model = Integration_server
        fields = ["datetime", "server", "update_type", "update_version", "status"]
        sequence = ["datetime", "server", "update_type", "update_version", "status"]
        attrs = {"class": "table table-striped"}