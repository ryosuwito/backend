# -*- coding: utf-8 -*-
import datetime

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.utils import timezone
from functools import partial
from django.core.exceptions import ValidationError

from .models import OnlineApplication, TestRequest, InternCandidate, OpenJob
from .types import (
    JobType,
    Workplace,
    JobPosition,
    OldJobPosition,
    JobPositionChoices,
    JobTypeChoices,
    JobWorkplaceChoices,
)


DateTimeInput = partial(forms.DateTimeInput, {'class': 'datetime', 'type': 'hidden'})


class OptionalChoiceWidget(forms.MultiWidget):
    def decompress(self, value):
        # this might need to be tweaked if the name of a
        # choice != value of a choice
        if value: # indicates we have a updating object versus new one
            if value in [x[0] for x in self.widgets[0].choices]:
                return [value, ""] # make it set the pulldown to choice
            else:
                return ["", value] # keep pulldown to blank, set freetext
        return ["", ""] # default for new object


class InfoSourceField(forms.MultiValueField):
    CAMPUS_TALK = "Campus Talk"
    CAMPUS_POSTER = "Campus Recruitment Poster"
    UNI_CAREER_WEB = "University Career Center Website"
    DEPARTMENT_CAREER_WEB = "Department Career Center Website"
    COMPANY_WEB = "Company Website"
    SCHOOL_EMAIL = "School Emails"
    FRIENDS = "Friends"
    BBS = "BBS"
    WECHAT = "WeChat"
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
        ("", "Others, please specify")
    )

    def __init__(self, label=None, choices=None, max_length=200, *args, **kwargs):
        """
        sets the two fields as not required but will
        enforce that (at least) one is set in compress
        """
        fields = (
            forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                choices=choices or InfoSourceField.INFO_SRC_CHOICES,
                required=False),
            forms.CharField(required=False))
        self.widget = OptionalChoiceWidget(widgets=[f.widget for f in fields])
        super(InfoSourceField,self).__init__(required=False, fields=fields, *args, **kwargs)
        self.label = label or 'Where do you get our recruitment information ? *'

    def compress(self, data_list):
        """
        generate and return value of the field from choicefield
        value and charfield value
        (if both empty, will throw exception
        """
        if not data_list:
            raise ValidationError('Please select at least one choice or specify in the text box')
        if not data_list[1] or data_list[1] == "":
            all_data = data_list[0]
        else:
            all_data = data_list[0] + [data_list[1]]
        return ','.join(all_data)


class OnlineApplicationForm(forms.ModelForm):
    start_time = forms.DateField(
        widget=forms.SelectDateWidget, label='Pick up a date to start working', initial=datetime.date.today(),
        help_text=('Note: After this day you need to work at least 3 months for a full-time internship or '
                   '4 months (3 days a week) for a part-time internship.')
    )

    position = forms.ChoiceField(choices=JobPositionChoices, label='Position*')
    OnlineAppChoices = tuple(filter(lambda x: x[0] != JobType.INTERNSHIP.name, JobTypeChoices))
    typ = forms.ChoiceField(choices=OnlineAppChoices, label='Type*')
    workplace = forms.ChoiceField(choices=JobWorkplaceChoices, label='Workplace*')

    resume = forms.FileField()
    info_src = InfoSourceField()

    class Meta:
        model = OnlineApplication
        fields = [
            'position', 'typ', 'workplace', 'start_time',
            'name', 'university', 'school', 'major',
            'email', 'resume', 'info_src',
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

    def __init__(self, *args, **kwargs):
        super(OnlineApplicationForm, self).__init__(*args, **kwargs)
        self.fields['resume'].help_text = 'Please make sure no chinese character in your file name'

    def clean_email(self):
        email = self.cleaned_data['email']
        applications = OnlineApplication.objects.filter(email=email)
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

    def clean(self):
        """
        Check if there is any (position, typ, workplace) job open or not.
        """
        queryset = OpenJob.objects.filter(active=True)

        open_positions = list({JobPosition[open_job.position].value for open_job in queryset})
        position = self.cleaned_data['position']
        open_jobs_with_position = queryset.filter(position=position)

        open_typs = list({JobType[open_job.typ].value for open_job in open_jobs_with_position})
        typ = self.cleaned_data['typ']
        open_jobs_with_typ = open_jobs_with_position.filter(typ=typ)

        open_workplaces = list({Workplace[open_job.workplace].value for open_job in open_jobs_with_typ})
        workplace = self.cleaned_data['workplace']
        open_jobs_with_workplace = open_jobs_with_typ.filter(workplace=workplace)

        if open_jobs_with_position.count() == 0:
            if len(open_positions) > 0:
                msg = "There is no open jobs for {} position. Open jobs only for {} position(s).".format(
                    JobPosition[position].value.lower(), ', '.join(open_positions).lower())
            else:
                msg = "There is no open jobs at the moment."

            self.add_error('position', msg)
        elif open_jobs_with_typ.count() == 0:
            msg = "There is no open {}. Open jobs for {} position are (one in) {}.".format(
                JobType[typ].value.lower(), JobPosition[position].value.lower(), ', '.join(open_typs).lower()
            )
            self.add_error('typ', msg)
        elif open_jobs_with_workplace.count() == 0:
            msg = "There is no open jobs in {}. Open jobs for {} {} only in {}.".format(
                Workplace[workplace].value, JobType[typ].value.lower(), JobPosition[position].value.lower(),
                ', '.join(open_workplaces),
            )
            self.add_error('workplace', msg)

        return self.cleaned_data


class InternApplicationForm(OnlineApplicationForm):
    position = forms.ChoiceField(
        choices=OldJobPosition.INTERN_POSITION_CHOICES.value,
        widget=forms.RadioSelect,
        initial=OldJobPosition.INTERN_POSITION_CHOICES.value[0][0])

    class Meta:
        model = OnlineApplication
        exclude = ['created_at', 'status']
        labels = {
            'name': _('Name *'),
            'email': _('Email *'),
        }
        widgets = {
            'position': forms.RadioSelect
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        valid = InternCandidate.objects.filter(email=email)
        if valid.count() == 0:
            raise forms.ValidationError(
                "This email is not valid for the position at the moment"
            )
        return email


class TestRequestForm(forms.ModelForm):
    class Meta:
        model = TestRequest
        exclude = ['hashstr', 'application', 'created_at', 'status', 'version', 'token', 'token_status']
        widgets = {
            'datetime': DateTimeInput()
        }

    def __init__(self, *args, **kwargs):
        super(TestRequestForm, self).__init__(*args, **kwargs)

    def clean_datetime(self):
        dt = self.cleaned_data['datetime']
        if dt < timezone.now():
            raise forms.ValidationError("The time has already passed")
        # weekno = dt.weekday()
        # if weekno >= 5:
        #     raise forms.ValidationError("Please choose weekday (Monday to Friday) only")
        return dt

    def clean(self):
        if self.instance and self.instance.pk:
            if not self.instance.allow_update():
                raise forms.ValidationError(
                    "You cannot change time of the test")
