# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-11-30 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20201117_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openjob',
            name='workplace',
            field=models.CharField(choices=[(b'HANOI', b'Hanoi'), (b'REMOTE', b'Remote'), (b'SHANGHAI', b'Shanghai'), (b'SINGAPORE', b'Singapore')], max_length=255),
        ),
    ]