# Generated by Django 2.2 on 2019-07-30 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0015_remove_backupinfo_backup_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mysqlinfo',
            name='backup_dir',
        ),
        migrations.RemoveField(
            model_name='mysqlinfo',
            name='backup_ip',
        ),
    ]
