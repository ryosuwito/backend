# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


PKU = 'PKU'
FDU = 'FDU'
SJTU = 'SJTU'
SITE_CHOICES = {
    (PKU, "北京大学"),
    (FDU, "复旦大学"),
    (SJTU, "上海交通大学")
}

SITE_CHOICES_MAP = dict((k, v) for k, v in SITE_CHOICES)


class Candidate(models.Model):
    PKU = 'PKU'
    FDU = 'FDU'
    SJTU = 'SJTU'
    SITE_CHOICES = (
        (PKU, "北京大学"),
        (FDU, "复旦大学"),
        (SJTU, "上海交通大学")
    )
    email = models.EmailField(max_length=100, unique=True)
    site = models.CharField(
        max_length=20,
        choices=SITE_CHOICES,
        default=PKU)
    name = models.CharField(max_length=100)
    university = models.CharField(max_length=100, null=True, blank=True)
    school = models.CharField(max_length=200, null=True, blank=True)
    major = models.CharField(max_length=200, null=True, blank=True)
    info_src = models.CharField(max_length=200, null=False, blank=False, default="N.A")

    def __str__(self):
        return self.email


class EventContent(models.Model):
    year = models.IntegerField(db_index=True)
    payload = models.TextField(blank=True, null=False, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
