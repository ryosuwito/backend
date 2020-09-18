# -*- coding: utf-8 -*-
from django import forms

from main.forms import OnlineApplicationForm

from main.types import (
    JobPosition,
    JobType,
    Workplace,
)

from .models import CampaignApplication


ALLOWED_JOBS = [JobPosition.FQRES, JobPosition.QRES]
ALLOWED_JOB_TYPES = [JobType.FULLTIME_JOB]
ALLOWED_WORKPLACE = [Workplace.SINGAPORE]

JobPositionChoices = [(pos.name, pos.value) for pos in ALLOWED_JOBS]
JobTypeChoices = [(job_type.name, job_type.value) for job_type in ALLOWED_JOB_TYPES]
WorkplaceChoices = [(wplace.name, wplace.value) for wplace in ALLOWED_WORKPLACE]


StatusType = CampaignApplication.StatusType
StatusChoices = [(stat.value, stat.value) for stat in StatusType]


class CampaignApplicationForm(OnlineApplicationForm):
    def __init__(self, *args, **kwargs):
        super(CampaignApplicationForm, self).__init__(*args, **kwargs)

    position = forms.ChoiceField(choices=JobPositionChoices, label='Position*')
    typ = forms.ChoiceField(choices=JobTypeChoices, label='Type*')
    workplace = forms.ChoiceField(choices=WorkplaceChoices, label='Workplace*')


class CampaignApplicationAdminForm(forms.ModelForm):
    class Meta:
        model = CampaignApplication
        fields = '__all__'

    status = forms.ChoiceField(choices=StatusChoices)
