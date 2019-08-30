# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-30 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20190529_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(choices=[(b'FULLTIME_INTERNSHIP', b'Full-time Internship'), (b'FULLTIME_JOB', b'Full-time Job'), (b'PARTTIME_INTERNSHIP', b'Part-time Internship')], db_index=True, max_length=255)),
                ('workplace', models.CharField(choices=[(b'REMOTE', b'Remote'), (b'SHANGHAI', b'Shanghai'), (b'SINGAPORE', b'Singapore')], max_length=255)),
                ('position', models.CharField(choices=[(b'DATA_ENGINEER', b'Data Engineer'), (b'DEV', b'Developer'), (b'FQRES', b'Fundamental Quantitative Researcher'), (b'OP_SPECIALIST', b'Operation Specialist'), (b'QRES', b'Quantitative Researcher')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='onlineapplication',
            name='start_time',
            field=models.DateField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='onlineapplication',
            name='typ',
            field=models.CharField(choices=[(b'FULLTIME_INTERNSHIP', b'Full-time Internship'), (b'FULLTIME_JOB', b'Full-time Job'), (b'PARTTIME_INTERNSHIP', b'Part-time Internship')], default=b'FULLTIME_JOB', max_length=255),
        ),
        migrations.AddField(
            model_name='onlineapplication',
            name='workplace',
            field=models.CharField(choices=[(b'REMOTE', b'Remote'), (b'SHANGHAI', b'Shanghai'), (b'SINGAPORE', b'Singapore')], default=b'SINGAPORE', max_length=255),
        ),
        migrations.AlterField(
            model_name='onlineapplication',
            name='position',
            field=models.CharField(choices=[(b'DATA_ENGINEER', b'Data Engineer'), (b'DEV', b'Developer'), (b'FQRES', b'Fundamental Quantitative Researcher'), (b'OP_SPECIALIST', b'Operation Specialist'), (b'QRES', b'Quantitative Researcher')], default=b'Developer', max_length=255),
        ),
        migrations.AlterIndexTogether(
            name='openjob',
            index_together=set([('typ', 'workplace')]),
        ),
    ]
