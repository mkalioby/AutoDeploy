# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0016_auto_20180807_1651'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunSQL(
            """insert into auth_permission (name, content_type_id, codename) values ("Can deploy project",10,"deploy_project");"""),
        migrations.RunSQL(
            """insert into auth_permission (name, content_type_id, codename) values ("Can clone project",10,"clone_project");"""),
        migrations.RunSQL(
            """insert into auth_permission (name, content_type_id, codename) values ("Can check server",9,"check_server");"""),
    ]
