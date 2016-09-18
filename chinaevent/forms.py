from django import forms
from chinaevent.models import Candidate


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data['email']
        candidates = Candidate.objects.filter(email=email)
        if candidates:
            raise forms.ValidationError("You already registered for the event.")
        return email
