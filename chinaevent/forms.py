from django import forms
from chinaevent.models import Candidate


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['site', 'email', 'name', 'university']

    def clean_email(self):
        email = self.cleaned_data['email']
        candidates = self.Meta.model.objects.filter(email=email)
        if candidates:
            raise forms.ValidationError("You already registered for the event.")
        return email
