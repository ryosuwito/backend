from django.utils.translation import ugettext_lazy as _
from django import forms
from django.utils import timezone
import datetime

from .models import OnlineApplication, TestRequest

from functools import partial
DateTimeInput = partial(forms.DateTimeInput, {'class': 'datetime', 'type': 'hidden'})


from django.core.exceptions import ValidationError
from django import forms


class OptionalChoiceWidget(forms.MultiWidget):
    def decompress(self, value):
        #this might need to be tweaked if the name of a choice != value of a choice
        if value: #indicates we have a updating object versus new one
            if value in [x[0] for x in self.widgets[0].choices]:
                 return [value,""] # make it set the pulldown to choice
            else:
                 return ["",value] # keep pulldown to blank, set freetext
        return ["",""] # default for new object


class InfoSourceField(forms.MultiValueField):
    CAMPUS_TALK = "Campus Talk"
    CAMPUS_POSTER = "Campus Recruitment Poster"
    UNI_CAREER_WEB = "University Career Center Website"
    DEPARTMENT_CAREER_WEB = "Department Career Center Website"
    COMPANY_WEB = "Company Website"
    SCHOOL_EMAIL = "School Emails"
    FRIENDS = "Friends"
    BBS = "BBS"
    INFO_SRC_CHOICES = (
        (CAMPUS_TALK, CAMPUS_TALK),
        (CAMPUS_POSTER, CAMPUS_POSTER),
        (UNI_CAREER_WEB, UNI_CAREER_WEB),
        (DEPARTMENT_CAREER_WEB, DEPARTMENT_CAREER_WEB),
        (COMPANY_WEB, COMPANY_WEB),
        (SCHOOL_EMAIL, SCHOOL_EMAIL),
        (FRIENDS, FRIENDS),
        (BBS, BBS),
        ("", "Others, please specify")
    )

    def __init__(self, label=None, choices=None, max_length=200, *args, **kwargs):
        """ sets the two fields as not required but will
            enforce that (at least) one is set in compress
        """
        fields = (forms.ChoiceField(widget=forms.RadioSelect,
                                    choices=choices or InfoSourceField.INFO_SRC_CHOICES,
                                    required=False),
                  forms.CharField(required=False))
        self.widget = OptionalChoiceWidget(widgets=[f.widget for f in fields])
        super(InfoSourceField,self).__init__(required=False, fields=fields, *args, **kwargs)
        self.label = label or 'Where do you get our recruitment information ? *'

    def compress(self, data_list):
        """ return the choicefield value if selected or charfield value
            (if both empty, will throw exception """
        if not data_list:
            raise ValidationError('Please select a choice or specify in text box')
        return data_list[0] or data_list[1]


class OnlineApplicationForm(forms.ModelForm):
    resume = forms.FileField()
    info_src = InfoSourceField()

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
        # weekno = dt.weekday()
        # if weekno >= 5:
        #     raise forms.ValidationError("Please choose weekday (Monday to Friday) only")
        return dt
