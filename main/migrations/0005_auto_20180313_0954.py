# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-13 01:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_onlineapplication_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineapplication',
            name='position',
            field=models.CharField(choices=[('DEV', 'Developer'), ('QRES', 'Quantitative Researcher'), ('FQRES', 'Fundamental Quantitative Researcher'), ('INTERN_QRES', 'Quantitative Researcher (Intern)')], default='DEV', max_length=20),
        ),
    ]
