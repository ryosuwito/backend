from django.utils.translation import ugettext_lazy as _
from django import forms
from main.models import OnlineApplication, TestRequest
from django.utils import timezone
import datetime

from functools import partial
DateTimeInput = partial(forms.DateTimeInput, {'class': 'datetime', 'type': 'hidden'})


class OnlineApplicationForm(forms.ModelForm):
    resume = forms.FileField()
    class Meta:
        model = OnlineApplication
        exclude = ['created_at', 'status']
        labels = {
                'name': _('Name *'),
                'position': _('Position *'),
                'email': _('Email *'),
        }


class TestRequestForm(forms.ModelForm):
    class Meta:
        model = TestRequest
        exclude = ['hashstr', 'application', 'created_at', 'status']
        widgets = {
            'datetime': DateTimeInput()
        }

    def __init__(self, *args, **kwargs):
        super(TestRequestForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            if self.instance.application.position == OnlineApplication.DEVELOPER:
                del self.fields['version']

    def clean_datetime(self):
        dt = self.cleaned_data['datetime']
        if dt < timezone.now():
            raise forms.ValidationError("The time has already passed")
        weekno = dt.weekday()
        if weekno >= 5:
            raise forms.ValidationError("Please choose weekday (Monday to Friday) only")
        return dt
