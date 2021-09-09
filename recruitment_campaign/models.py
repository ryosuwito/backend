# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import enum
import uuid
import os

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
    # file will be uploaded to MEDIA_ROOT/resumes/{email}_filename
    _, extension = os.path.splitext(filename)
    if extension:
        return "campaign/resumes/{}_{}{}".format(instance.email, uuid.uuid4(), extension)
    else:
        return "campaign/resumes/{}_{}".format(instance.email, uuid.uuid4())


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


class ApplicationStatus(enum.Enum):
    NEW = "NEW"
    PASS_RESUME = "PASS_RESUME"
    FAIL_RESUME = "FAIL_RESUME"


class CampaignOnlineApplication(models.Model):
    typ = models.CharField(max_length=255)
    workplace = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    name = models.CharField(max_length=30)
    university = models.CharField(max_length=100, null=True, blank=True)
    school = models.CharField(max_length=200, null=True, blank=True)
    major = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    resume = models.FileField(max_length=100, blank=True,
                              upload_to=user_resume_path)
    info_src = models.CharField(max_length=200, null=False, blank=False, default="N.A")

    start_time = models.DateField(max_length=255, blank=True, null=True)

    # Additional fields for admin management
    status = models.CharField(
        max_length=20,
        default=ApplicationStatus.NEW.name)
    created_at = models.DateTimeField(auto_now_add=True)

    need_work_pass = models.CharField(max_length=32, blank=True, default='Yes')

    def __unicode__(self):
        return self.email

    @property
    def get_position_display(self):
        return self.position.replace('_', ' ')

    @property
    def get_type_display(self):
        return self.typ.replace('_', ' ')

    @property
    def get_workplace_display(self):
        return self.workplace.replace('_', ' ')
