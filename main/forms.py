from django import forms
from main.models import OnlineApplication, TestRequest
from datetimewidget.widgets import DateWidget, TimeWidget
import datetime

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class OnlineApplicationForm(forms.ModelForm):
    resume = forms.FileField()
    class Meta:
        model = OnlineApplication
        exclude = ['created_at', 'status']

    def clean_email(self):
        email = self.cleaned_data['email']
        # TODO: check if email existed
        if email == "a@dytechlab.com":
            raise forms.ValidationError("You already submit the application")
        return email


class TestRequestForm(forms.ModelForm):
    class Meta:
        model = TestRequest
        exclude = ['hashstr', 'application', 'time', 'created_at', 'status']
        widgets = {
            'date': DateInput()
        }

