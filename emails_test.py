import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dtlweb.settings'
import django
django.setup()

from django.core.mail import EmailMessage, BadHeaderError
from main.models import OnlineApplication, TestRequest
from main.emails import send_online_application_confirm

if __name__ == "__main__":
    application = OnlineApplication.objects.get(pk=1)
    send_online_application_confirm(application)
