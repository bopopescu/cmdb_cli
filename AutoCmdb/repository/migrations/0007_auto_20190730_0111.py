# Generated by Django 2.2 on 2019-07-30 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0006_mysqlinfo_master_port'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mysqlinfo',
            name='master_port',
            field=models.IntegerField(null=True),
        ),
    ]