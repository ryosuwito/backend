# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-13 03:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180313_0954'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternCandidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chinese_name', models.CharField(max_length=30)),
                ('english_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=100, unique=True)),
            ],
        ),
    ]