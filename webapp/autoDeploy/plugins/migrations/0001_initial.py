# Generated by Django 2.2.16 on 2020-11-15 09:00

import datetime
from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL("""DROP TABLE IF EXISTS Plugins;"""),
        migrations.CreateModel(
            name='Plugins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('settings', jsonfield.fields.JSONField(db_column='settings', default={})),
                ('created_on', models.DateTimeField(blank=True, default=datetime.datetime.now())),
            ],
            options={
                'db_table': 'Plugins',
                'get_latest_by': 'id',
            },
        ),
    ]