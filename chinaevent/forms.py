# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.utils.translation import ugettext_lazy as _
from django import forms
from chinaevent.models import Candidate
from main.forms import InfoSourceField
from main.models import OnlineApplication
from main.types import (
    JobPosition,
    JobType,
)


CAMPUS_TALK = "校园宣讲会"
CAMPUS_POSTER = "校园宣传海报"
UNI_CAREER_WEB = "学校招聘信息"
DEPARTMENT_CAREER_WEB = "学院招聘网站"
COMPANY_WEB = "公司官网"
SCHOOL_EMAIL = "电子邮件宣传"
FRIENDS = "朋友推荐"
BBS = "校园BBS"
WECHAT = 'WeChat'
INFO_SRC_CHOICES = (
    (CAMPUS_TALK, CAMPUS_TALK),
    (CAMPUS_POSTER, CAMPUS_POSTER),
    (UNI_CAREER_WEB, UNI_CAREER_WEB),
    (DEPARTMENT_CAREER_WEB, DEPARTMENT_CAREER_WEB),
    (COMPANY_WEB, COMPANY_WEB),
    (SCHOOL_EMAIL, SCHOOL_EMAIL),
    (FRIENDS, FRIENDS),
    (BBS, BBS),
    (WECHAT, WECHAT),
    ("", "其他，请注明")
)


EVENT_JOB_CHOICES = (
    (JobPosition.DEV.name, JobPosition.DEV.value),
    (JobPosition.QRES.name, JobPosition.QRES.value),
    (JobPosition.FQRES.name, JobPosition.FQRES.value),
)


class RegistrationForm(forms.ModelForm):
    position = forms.ChoiceField(label='Position*', choices=EVENT_JOB_CHOICES)
    info_src = InfoSourceField(choices=INFO_SRC_CHOICES,
                               label="你从哪里得到我们的招聘信息* (多选)")
    resume = forms.FileField(label='Resume*')
    typ = forms.ChoiceField(label='Type*', choices=[
        (JobType.FULLTIME_JOB.name, JobType.FULLTIME_JOB.value),
        (JobType.INTERNSHIP.name, JobType.INTERNSHIP.value),
    ])

    class Meta:
        model = OnlineApplication
        fields = [
            'position', 'typ',
            'email', 'name', 'university', 'school', 'major', 'resume', 'info_src',
        ]
        labels = {
            'email': _('Email*'),
            'name': _('Name*'),
            'university': _('University'),
            'school': _('School'),
            'major': _('Major'),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        candidates = self.Meta.model.objects.filter(email=email)
        if candidates:
            raise forms.ValidationError("You already registered for the event.")
        return email


class OnsiteRegistrationForm(forms.ModelForm):
    test_site = forms.ChoiceField(
        choices=Candidate.SITE_CHOICES)

    class Meta:
        model = OnlineApplication
        fields = [
            'test_site'
        ]
        labels = {
            'test_site': _('Written Test Site'),
        }
