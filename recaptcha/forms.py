from django.contrib.admin.forms import AdminAuthenticationForm as _AdminAuthenticationForm
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class AdminAuthenticationForm(_AdminAuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
