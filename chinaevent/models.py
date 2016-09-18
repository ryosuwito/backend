from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    university = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return self.email
