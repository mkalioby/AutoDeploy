# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0002_permissions'),
    ]

    operations = [
        migrations.RunSQL("""
        DROP PROCEDURE IF EXISTS MigrateData;
        CREATE PROCEDURE MigrateData()
        BEGIN
            IF (SELECT count(*) FROM information_schema.TABLES WHERE TABLE_NAME = 'autodeploy_plugins') > 0
            THEN
                insert into Plugins (name, settings) 
                select `name`, `settings`
                from autodeploy_plugins;
            END IF;
            
            
            IF (SELECT count(*) FROM information_schema.TABLES WHERE TABLE_NAME = 'autodeploy_server') > 0 THEN
                insert into Server (name, ip, port, DNS) 
                select name, ip, port, DNS
                from autodeploy_server;
            END IF;
            
            IF (SELECT count(*) FROM information_schema.TABLES WHERE TABLE_NAME = 'autodeploy_sshkey') > 0 THEN
                insert into SSHKey (`name`, `key`) 
                select `name`, `key`
                from autodeploy_sshkey ;
            END IF;
            
            IF (SELECT count(*) FROM information_schema.TABLES WHERE TABLE_NAME = 'autodeploy_project') > 0 THEN
                insert into deployment_project (name, repo_type, repo, update_style, lastCommit, lastTag, lastCommitDate, working_dir, configFile, lastUpdate, repo_link, deployment_link, newVersion, emailUsers, autoDeploy, default_branch, default_server_id, sshKey_id) 
                select name, repo_type, repo, update_style, lastCommit, lastTag, lastCommitDate, working_dir, configFile, lastUpdate, repo_link, deployment_link, newVersion, emailUsers, autoDeploy, default_branch, default_server_id, sshKey_id 
                from autodeploy_project ;
            END IF;
            
            IF (SELECT count(*) FROM information_schema.TABLES WHERE TABLE_NAME = 'autodeploy_deployment_server') > 0 THEN
                insert into Deployment_Server (datetime, update_type, update_version, has_new_version, project_id, server_id, deployed ) 
                select datetime, update_type, update_version, has_new_version, project_id, server_id, deployed 
                from autodeploy_deployment_server ;
            END IF;
            
            IF (SELECT count(*) FROM information_schema.TABLES WHERE TABLE_NAME = 'autodeploy_user_project') > 0 THEN
                insert into User_Project (project_id, user_id) 
                select project_id, user_id
                from autodeploy_user_project;
            END IF;
        END;
        CALL MigrateData;
        DROP PROCEDURE IF EXISTS MigrateData;
        """)
    ]
