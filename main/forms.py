from django import forms

class TestRequestForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput)
    university = forms.CharField(label="University", widget=forms.TextInput)
    major = forms.CharField(label="Major", widget=forms.TextInput)
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
