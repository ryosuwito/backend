# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-09-04 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chinaevent', '0005_candidate_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(db_index=True)),
                ('payload', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
