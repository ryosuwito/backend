# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import enum

from django.db import models

from main.models import OnlineApplication

# Create your models here.


class Campaign(models.Model):
    name = models.CharField(max_length=255)
    meta_data = models.TextField(blank=True, default="{}")
    starttime = models.DateTimeField()
    test_id = models.IntegerField()
    active = models.BooleanField(blank=True, default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def user_resume_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/campaign/resumes/{email}_filename
    return "campaign/resumes/{}_{}".format(instance.email, filename)


class CampaignApplication(models.Model):

    class StatusType(enum.Enum):
        new = 'new'
        passed_resume = 'passed_resume'
        refused_resume = 'refused_resume'
        invited = 'invited'
        refuse_invitation = 'refuse_invitation'
        accept_invitation = 'accept_invitation'

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='applications')
    application = models.ForeignKey(
        OnlineApplication,
        on_delete=models.CASCADE,
        related_name='campain_applications',
    )

    # new -> passed_resume
    # new -> failed_resume
    status = models.CharField(max_length=255, blank=True, default='new')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
