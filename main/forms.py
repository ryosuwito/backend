from django.utils.translation import ugettext_lazy as _
from django import forms
from main.models import OnlineApplication, TestRequest
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
