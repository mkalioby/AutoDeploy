# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodeploy', '0016_auto_20180807_1651'),
    ]

    operations = [
        migrations.RunSQL(
            """insert into auth_permission (name, content_type_id, codename) values ("Can deploy project",10,"deploy_project");"""),
        migrations.RunSQL(
            """insert into auth_permission (name, content_type_id, codename) values ("Can clone project",10,"clone_project");"""),
        migrations.RunSQL(
            """insert into auth_permission (name, content_type_id, codename) values ("Can check server",9,"check_server");"""),
    ]
