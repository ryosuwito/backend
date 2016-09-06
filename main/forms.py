from django import forms
from main.models import TestRequest
from datetimewidget.widgets import DateWidget, TimeWidget

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class TestRequestForm(forms.ModelForm):
    class Meta:
        model = TestRequest
        exclude = ['created_at', 'status']
        # widgets = {
        #     'date': DateWidget(usel10n=True, bootstrap_version=3),
        #     'time': TimeWidget(usel10n=True, bootstrap_version=3)
        # }

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == "a@email.com":
            raise forms.ValidationError("Email is in use. Please see your email to change request.")
        return email


