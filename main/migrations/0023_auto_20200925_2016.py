# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-09-25 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20200925_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlineapplication',
            name='need_work_pass',
            field=models.CharField(blank=True, default='Yes', max_length=32),
        ),
        migrations.AddField(
            model_name='testrequest',
            name='note',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='onlineapplication',
            name='position',
            field=models.CharField(default=b'DEV', max_length=255),
        ),
        migrations.AlterField(
            model_name='onlineapplication',
            name='status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('PASS_RESUME', 'PASS RESUME'), ('FAIL_RESUME', 'FAIL RESUME'), ('PASS_TEST', 'PASS TEST'), ('FAIL_TEST', 'FAIL TEST'), ('DNF_TEST', 'DNF TEST'), ('campaign', 'From campagins')], default='NEW', max_length=20),
        ),
    ]