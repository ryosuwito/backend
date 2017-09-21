# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django import forms
from chinaevent.models import Candidate
from main.forms import InfoSourceField


CAMPUS_TALK = "校园宣讲会"
CAMPUS_POSTER = "校园宣传海报"
UNI_CAREER_WEB = "学校招聘信息"
DEPARTMENT_CAREER_WEB = "学院招聘网站"
COMPANY_WEB = "公司官网"
SCHOOL_EMAIL = "电子邮件宣传"
FRIENDS = "朋友推荐"
BBS = "校园BBS"
INFO_SRC_CHOICES = (
    (CAMPUS_TALK, CAMPUS_TALK),
    (CAMPUS_POSTER, CAMPUS_POSTER),
    (UNI_CAREER_WEB, UNI_CAREER_WEB),
    (DEPARTMENT_CAREER_WEB, DEPARTMENT_CAREER_WEB),
    (COMPANY_WEB, COMPANY_WEB),
    (SCHOOL_EMAIL, SCHOOL_EMAIL),
    (FRIENDS, FRIENDS),
    (BBS, BBS),
    ("", "其他，请注明")
)

class RegistrationForm(forms.ModelForm):
    info_src = InfoSourceField(choices=INFO_SRC_CHOICES,
                                label="你从哪里得到我们的招聘信息* (多选)")
    class Meta:
        model = Candidate
        fields = ['site', 'email', 'name', 'university', 'major', 'info_src']
        labels = {
            'site': _('笔试地点*'),
            'email': _('电子邮箱*'),
            'name': _('姓名*'),
            'university': _('学校'),
            'major': _('专业'),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        candidates = self.Meta.model.objects.filter(email=email)
        if candidates:
            raise forms.ValidationError("You already registered for the event.")
        return email
