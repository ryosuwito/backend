# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-15 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('site', models.CharField(choices=[('PKU', 'PKU'),
                                                   ('SJTU', 'SJTU'),
                                                   ('FDU', 'FDU')],
                                          default='PKU',
                                          max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('university', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
