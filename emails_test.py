import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dtlweb.settings'
import django
django.setup()

from django.core.mail import EmailMessage, BadHeaderError
from main.models import OnlineApplication, TestRequest
from main.emails import *

if __name__ == "__main__":
    application = OnlineApplication.objects.get(pk=4)
    test_request = TestRequest.objects.get(pk=4)
    print 'send online application confirm'
    send_online_application_confirm(application)
    print 'send summary'
    send_online_application_summary(application)
    print 'send test request'
    send_test_request(test_request);
    # print 'send test'
    # send_test(test_request);
