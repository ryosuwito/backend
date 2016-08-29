from django import forms

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class TestRequestForm(forms.Form):
    POSTION_CHOICES = (
        ("Researcher", "Researcher"),
        ("Developer", "Developer")
    )
    position = forms.ChoiceField(choices=POSTION_CHOICES, label="Position")
    name = forms.CharField(label="Name", widget=forms.TextInput)
    university = forms.CharField(label="University", widget=forms.TextInput)
    major = forms.CharField(label="Major", widget=forms.TextInput)
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    date = forms.DateField(label="Preferred Date", widget=DateInput())
