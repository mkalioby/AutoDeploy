import django_tables2 as Table
import django_tables2.tables as tables
from django_tables2.export.views import ExportMixin
from .models import Plugins


class PluginsTable(ExportMixin, tables.Table):
    Operations = Table.TemplateColumn("<a href='{% url 'edit_plugin' record.id %}'><span class='fa fa-edit' title='Edit'></span></a>&nbsp;&nbsp;<a href='{% url 'delete_plugin' record.id %}'><span class='fa fa-trash' title='Delete'></span></a>")
    class Meta:
        model = Plugins
        attrs = {"class": "table table-striped"}
        fields = ["name", "Operations"]
