# Generated by Django 2.2 on 2019-07-30 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0011_remove_mysqlinfo_archive_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='mysqlinfo',
            name='BP_size',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mysqlinfo',
            name='backup_dir',
            field=models.CharField(max_length=128, null=True),
        ),
    ]