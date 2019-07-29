# Generated by Django 2.2 on 2019-07-29 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_auto_20190729_0526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instanceinfo',
            old_name='db_username',
            new_name='db_name',
        ),
        migrations.AlterUniqueTogether(
            name='instanceinfo',
            unique_together={('max_tablename', 'db_name', 'db_ip', 'port')},
        ),
    ]