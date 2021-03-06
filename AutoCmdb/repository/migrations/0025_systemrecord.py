# Generated by Django 2.2 on 2019-08-05 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0024_remove_mysqlinfo_root_pass'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=50)),
                ('ip', models.GenericIPAddressField()),
                ('service_name', models.CharField(max_length=10)),
                ('useful', models.CharField(max_length=50, null=True)),
                ('realm_name', models.CharField(default='', max_length=256)),
                ('status', models.CharField(default='', max_length=16)),
            ],
            options={
                'db_table': 'SystemRecord',
                'unique_together': {('hostname', 'ip')},
            },
        ),
    ]
