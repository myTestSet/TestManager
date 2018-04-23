# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-10 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('create_time', models.DateTimeField(auto_created=True, auto_now=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=1024)),
                ('department', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'account_user',
            },
        ),
    ]
