from __future__ import unicode_literals

from django.db import models


class Candidate(models.Model):
    PKU = 'PKU'
    SJTU = 'SJTU'
    FDU = 'FDU'
    SITE_CHOICES = (
        (PKU, "PKU"),
        (SJTU, "SJTU"),
        (FDU, "FDU")
    )
    email = models.EmailField(max_length=100, unique=True)
    site = models.CharField(
        max_length=20,
        choices=SITE_CHOICES,
        default=PKU)
    name = models.CharField(max_length=100)
    university = models.CharField(max_length=100, null=True, blank=True)
    major = models.CharField(max_length=200, null=True, blank=True)
    info_src = models.CharField(max_length=200, null=False, blank=False, default="N.A")

    def __str__(self):
        return self.email
