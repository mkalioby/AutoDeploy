# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """ 
            insert into auth_permission (name, content_type_id, codename) 
            select "Can check server",id,"check_server" from django_content_type where model = 'server';
            
            insert into auth_permission (name, content_type_id, codename) 
            select "Can clone project",id,"clone_project" from django_content_type where model = 'project';
        
            insert into auth_permission (name, content_type_id, codename) 
            select "Can deploy project",id,"deploy_project" from django_content_type where model = 'project';
            """),
    ]
