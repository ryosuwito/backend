# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-21 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chinaevent', '0003_candidate_info_src'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='site',
            field=models.CharField(choices=[('PKU', '\u5317\u4eac\u5927\u5b66'), ('FDU', '\u590d\u65e6\u5927\u5b66'), ('SJTU', '\u4e0a\u6d77\u4ea4\u901a\u5927\u5b66')], default='PKU', max_length=20),
        ),
    ]
