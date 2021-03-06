# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-09-25 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20200728_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigEntry',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('value', models.CharField(blank=True, default='', max_length=255)),
                ('extra', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='openjob',
            name='position',
            field=models.CharField(choices=[(b'DATA_ANALYST', b'Data Analyst'),
                                            (b'DATA_ENGINEER', b'Data Engineer'),
                                            (b'DEV', b'Developer'),
                                            (b'FPGA_ENGINEER', b'FPGA Engineer'),
                                            (b'FSDEV', b'Full-Stack Developer'),
                                            (b'FQRES', b'Fundamental Quantitative Researcher'),
                                            (b'OP_SPECIALIST', b'Operation Specialist'),
                                            (b'QRES', b'Quantitative Researcher'),
                                            (b'SYSAD', b'System Administrator')],
                                   max_length=255),
        ),
        migrations.AlterField(
            model_name='openjob',
            name='typ',
            field=models.CharField(choices=[(b'FULLTIME_JOB', b'Full-time'),
                                            (b'FULLTIME_INTERNSHIP', b'Full-time Internship'),
                                            (b'INTERNSHIP', b'Internship'),
                                            (b'PARTTIME_INTERNSHIP', b'Part-time Internship')],
                                   max_length=255),
        ),
    ]
