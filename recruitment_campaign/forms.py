# -*- coding: utf-8 -*-
import datetime

from django.utils.translation import ugettext_lazy as _
from django import forms

from main.forms import InfoSourceField

from main.types import (
    JobPosition,
    JobType,
    Workplace,
)

from .models import (
    CampaignApplication,
    CampaignOnlineApplication,
)


ALLOWED_JOBS = [JobPosition.FQRES, JobPosition.QRES]
ALLOWED_JOB_TYPES = [JobType.FULLTIME_JOB]
ALLOWED_WORKPLACE = [Workplace.SINGAPORE]

JobPositionChoices = [(pos.name, pos.value) for pos in ALLOWED_JOBS]
JobTypeChoices = [(job_type.name, job_type.value) for job_type in ALLOWED_JOB_TYPES]
WorkplaceChoices = [(wplace.name, wplace.value) for wplace in ALLOWED_WORKPLACE]


StatusType = CampaignApplication.StatusType
StatusChoices = [(stat.value, stat.value) for stat in StatusType]


class CampaignApplicationForm(forms.ModelForm):
    start_time = forms.DateField(
        widget=forms.SelectDateWidget, label='I can start working on', initial=datetime.date.today(),
    )

    resume = forms.FileField()
    info_src = InfoSourceField()

    class Meta:
        model = CampaignOnlineApplication
        fields = [
            'position',
            'typ',
            'workplace',
            'start_time',
            'name',
            'university',
            'school',
            'major',
            'email',
            'resume',
            'info_src',
        ]
        labels = {
            'name': _('Name *'),
            'position': _('Position*'),
            'email': _('Email*'),
            'typ': _('Type*'),
            'workplace': _('Workplace*'),
        }
        help_texts = {
            'email': 'Please avoid using QQ mailbox.',
        }

    def __init__(self, campaign, *args, **kwargs):
        super(CampaignApplicationForm, self).__init__(*args, **kwargs)
        self.fields['resume'].help_text = 'Please make sure no chinese character in your file name'

        self.fields['position'] = forms.ChoiceField(
            choices=map(lambda x: (x, x.replace('_', ' ')), campaign.get('position')), label='Position*')
        self.fields['typ'] = forms.ChoiceField(
            choices=map(lambda x: (x, x.replace('_', ' ')), campaign.get('type')), label='Type*')
        self.fields['workplace'] = forms.ChoiceField(
            choices=map(lambda x: (x, x.replace('_', ' ')), campaign.get('workplace')), label='Workplace*')

    def clean_email(self):
        email = self.cleaned_data['email']
        applications = CampaignOnlineApplication.objects.filter(email=email)
        if applications.count() > 0:
            position = applications.first().get_position_display
            raise forms.ValidationError(
                "You've already applied for %s position before." % position
            )
        return email

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time is not None and start_time < datetime.date.today():
            raise forms.ValidationError(
                "Too early to start."
            )

        return start_time


class CampaignApplicationAdminForm(forms.ModelForm):
    class Meta:
        model = CampaignApplication
        fields = '__all__'

    status = forms.ChoiceField(choices=StatusChoices)
