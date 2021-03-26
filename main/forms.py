# -*- coding: utf-8 -*-
import datetime
import json

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.utils import timezone
from functools import partial
from django.core.exceptions import ValidationError

from .models import (
    OnlineApplication,
    TestRequest,
    InternCandidate,
    OpenJob,
    ConfigEntry,
)
from .types import (
    OldJobPosition,
    ConfigKey,
)


DateTimeInput = partial(forms.DateTimeInput, {'class': 'datetime', 'type': 'hidden'})


def get_type_in_database_config(name):
    config_entry = ConfigEntry.objects.get(name=name)
    types = json.loads(config_entry.extra)
    return types


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

    resume = forms.FileField()
    info_src = InfoSourceField()

    need_work_pass = forms.CharField(
        label='Do you need a work pass to work in Singapore?',
        widget=forms.RadioSelect(choices=(('Yes', 'Yes'), ('No', 'No'))),
        required=False,
    )

    class Meta:
        model = OnlineApplication
        fields = [
            'position',
            'typ',
            'workplace',
            'need_work_pass',
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

    def __init__(self, *args, **kwargs):
        super(OnlineApplicationForm, self).__init__(*args, **kwargs)
        self.fields['resume'].help_text = 'Please make sure no chinese character in your file name'

        self.position_map = get_type_in_database_config(ConfigKey.JOB_POSITION.value)
        self.type_map = get_type_in_database_config(ConfigKey.JOB_TYPE.value)
        self.workplace_map = get_type_in_database_config(ConfigKey.JOB_WORKPLACE.value)
        self.open_jobs = OpenJob.objects.filter(active=True)

        self.position_choices = list(
            map(
                lambda x: [x, self.position_map.get(x)],
                set(map(lambda x: x.position, self.open_jobs))
            )
        )
        self.fields['position'] = forms.ChoiceField(choices=self.position_choices, label='Position*')

        self.type_choices = list(
            map(
                lambda x: [x, self.type_map.get(x)],
                set(map(lambda x: x.typ, self.open_jobs))
            )
        )
        self.fields['typ'] = forms.ChoiceField(choices=self.type_choices, label='Type*')

        # TODO didn't filter workplace for quick use
        self.workplace_choices = self.workplace_map.items()
        self.fields['workplace'] = forms.ChoiceField(choices=self.workplace_choices, label='Workplace*')

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
        queryset = self.open_jobs

        open_positions = list(map(lambda x: x[1], self.position_choices))
        position = self.cleaned_data['position']
        open_jobs_with_position = queryset.filter(position=position)

        open_typs = list({self.type_map.get(open_job.typ) for open_job in open_jobs_with_position})
        typ = self.cleaned_data['typ']
        open_jobs_with_typ = open_jobs_with_position.filter(typ=typ)

        open_workplaces = []
        for open_job in open_jobs_with_typ:
            open_workplaces.extend(open_job.workplace.split(','))

        open_workplaces = list(set(map(lambda x: self.workplace_map.get(x), open_workplaces)))
        workplace = self.cleaned_data['workplace']
        open_jobs_with_workplace = open_jobs_with_typ.filter(workplace__contains=workplace)

        if open_jobs_with_position.count() == 0:
            if len(open_positions) > 0:
                msg = "There is no open jobs for {} position. Open jobs only for {} position(s).".format(
                    self.position_map[position], ', '.join(open_positions).lower())
            else:
                msg = "There is no open jobs at the moment."

            self.add_error('position', msg)
        elif open_jobs_with_typ.count() == 0:
            msg = "There is no open {}. Open jobs for {} position are (one in) {}.".format(
                self.type_map[typ], self.position_map[position], ', '.join(open_typs).lower()
            )
            self.add_error('typ', msg)
        elif open_jobs_with_workplace.count() == 0:
            msg = "There is no open jobs in {}. Open jobs for {} {} only in {}.".format(
                self.workplace_map[workplace], self.type_map[typ], self.position_map[position],
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


class OpenJobForm(forms.ModelForm):
    class Meta:
        model = OpenJob
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OpenJobForm, self).__init__(*args, **kwargs)
        self.fields['position'] = forms.ChoiceField(
            choices=get_type_in_database_config(ConfigKey.JOB_POSITION.value).items())

        self.fields['typ'] = forms.ChoiceField(
            choices=get_type_in_database_config(ConfigKey.JOB_TYPE.value).items())

        workplace_items = get_type_in_database_config(ConfigKey.JOB_WORKPLACE.value).items()
        workplace_len = len(workplace_items)
        workplace_choices = []
        for i in range(1, 2**workplace_len):
            bi = "{0:20b}".format(i)[-workplace_len:]
            item_arr = list(filter(lambda x: x[0] == '1', zip(list(bi), workplace_items)))
            label = ','.join(map(lambda x: x[1][0], item_arr))
            value = ','.join(map(lambda x: x[1][1], item_arr))
            workplace_choices.append([label, value])
        workplace_choices = sorted(workplace_choices, key=lambda x: (len(x[0]), x[0]))
        self.fields['workplace'] = forms.ChoiceField(choices=workplace_choices)

    def clean_description(self):
        try:
            cleaned_data = self.cleaned_data['description']
            json.loads(cleaned_data)
        except Exception:
            self.add_error('description', 'Not a valid JSON.')

        return cleaned_data
