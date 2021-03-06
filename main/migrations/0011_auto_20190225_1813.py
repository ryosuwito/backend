# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-25 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20180919_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineapplication',
            name='position',
            field=models.CharField(choices=[('DEV', 'Developer'),
                                            ('DATA_ENGINEER', 'Data Engineer'),
                                            ('OP_SPECIALIST', 'Trading Operation Specialist'),
                                            ('QRES', 'Quantitative Researcher'),
                                            ('FQRES', 'Fundamental Quantitative Researcher'),
                                            ('INTERN_QRES', 'Quantitative Researcher (Internship)'),
                                            ('INTERN_DATA_ENGINEER', 'Data Engineer (Internship)')],
                                   default='DEV',
                                   max_length=20),
        ),
    ]
