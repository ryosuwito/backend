import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dtlweb.settings'
import django
django.setup()

from django.core.mail import EmailMessage, BadHeaderError
from main.models import TestRequest


class EmailHelper(object):

    def __init__(self):
        pass

    @staticmethod
    def send_test_request_confirm(test_request):
        pass

    @staticmethod
    def send_test_to_candidate(test_request):
        message = EmailMessage()
        message.content_subtype = "html"
        message.subject = "DTL Test"
        message.body = "<p>Hi {},</p> <p>please see the test file here.</p>"\
                .format(test_request.name)
        message.attach_file('./manage.py') # path to test file
        message.to = [test_request.email,]
        message.bcc = ['ynguyen@dytechlab.com',]

        try:
            message.send()
        except BadHeaderError:
            # TODO: log error here
            print 'BadHeaderError. Email is not sent.'


def test():
    test_request = TestRequest(
        position=TestRequest.DEVELOPER,
        name="Yen",
        university="NTU",
        major="Computer Science",
        email="ynguyen@dytechlab.com",
        date="2015-05-05",
        time="09:09",
        version=TestRequest.VER_ENGLISH,
        created_at="2015-04-05",
        status=TestRequest.STATUS_PENDING
    )
    # EmailHelper.send_test_to_candidate(test_request)


