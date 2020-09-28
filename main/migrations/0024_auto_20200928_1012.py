# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-09-28 02:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20200925_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openjob',
            name='position',
            field=models.CharField(choices=[(b'DATA_ANALYST', b'Data Analyst'), (b'DATA_ENGINEER', b'Data Engineer'), (b'DEV', b'Developer'), (b'FPGA_ENGINEER', b'FPGA Engineer'), (b'FSDEV', b'Full-Stack Developer'), (b'FQRES', b'Fundamental Quantitative Researcher'), (b'QRES', b'Quantitative Researcher'), (b'SYSAD', b'System Administrator'), (b'OP_SPECIALIST', b'Trading Support Engineer')], max_length=255),
        ),
    ]
