from django import forms
from main.models import OnlineApplication, TestRequest
from datetimewidget.widgets import DateWidget, TimeWidget

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class OnlineApplicationForm(forms.ModelForm):
    resume = forms.FileField()
    class Meta:
        model = OnlineApplication
        exclude = ['created_at', 'status', 'resume']


    def clean_email(self):
        # TODO: check if email existed
        email = self.cleaned_data['email']
        if email == "a@email.com":
            raise forms.ValidationError("Email is in use. Please see your email to change request.")
        return email



class TestRequestForm(forms.ModelForm):
    class Meta:
        model = TestRequest
        exclude = ['signature', 'application', 'created_at', 'status']



