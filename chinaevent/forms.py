# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django import forms
from chinaevent.models import Candidate
from main.forms import InfoSourceField


CAMPUS_TALK = u"大学 Ca"
CAMPUS_POSTER = "Campus Recruitment Poster"
UNI_CAREER_WEB = "University Career Center Website"
DEPARTMENT_CAREER_WEB = "Department Career Center Website"
COMPANY_WEB = "Company Website"
SCHOOL_EMAIL = "School Emails"
FRIENDS = "Friends"
BBS = "BBS"
INFO_SRC_CHOICES = (
    (CAMPUS_TALK, CAMPUS_TALK),
    (CAMPUS_POSTER, CAMPUS_POSTER),
    (UNI_CAREER_WEB, UNI_CAREER_WEB),
    (DEPARTMENT_CAREER_WEB, DEPARTMENT_CAREER_WEB),
    (COMPANY_WEB, COMPANY_WEB),
    (SCHOOL_EMAIL, SCHOOL_EMAIL),
    (FRIENDS, FRIENDS),
    (BBS, BBS),
    ("", "Others, please specify")
)

class RegistrationForm(forms.ModelForm):
    info_src = InfoSourceField(choices=INFO_SRC_CHOICES)
    class Meta:
        model = Candidate
        fields = ['site', 'email', 'name', 'university', 'major', 'info_src']
        labels = {
            'site': _('现场 *'),
            'email': _('Email *'),
            'name': _('Name *'),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        candidates = self.Meta.model.objects.filter(email=email)
        if candidates:
            raise forms.ValidationError("You already registered for the event.")
        return email
