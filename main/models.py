from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from main.hashes import gen_hashstr
from main.emails import send_test_request
import datetime


def user_resume_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/{email}_filename
    return '{}_{}'.format(instance.email, filename)


class OnlineApplication(models.Model):
    DEVELOPER = "Dev"
    Q_RESEARCHER = "QRes"
    FQ_RESEARCHER = "FQRes"
    POSITION_CHOICES = (
        (DEVELOPER, "Developer"),
        (Q_RESEARCHER, "Quantitative Researcher"),
        (FQ_RESEARCHER, "Fundamental Quantitative Researcher"),
    )

    APP_STATUS_NEW = "NEW"
    APP_STATUS_PASS_RESUME = "PASS_RESUME"
    APP_STATUS_FAIL_RESUME = "FAIL_RESUME"
    APP_STATUS_PASS_TEST = "PASS_TEST"
    APP_STATUS_FAIL_TEST = "FAIL_TEST"
    APP_STATUS_CHOICES = (
        (APP_STATUS_NEW, "NEW"),
        (APP_STATUS_PASS_RESUME, "PASS_RESUME"),
        (APP_STATUS_FAIL_RESUME, "FAIL_RESUME"),
        (APP_STATUS_PASS_TEST, "PASS_TEST"),
        (APP_STATUS_FAIL_TEST, "FAIL_TEST"),
    )

    position = models.CharField(
            max_length=20,
            choices=POSITION_CHOICES,
            default=DEVELOPER)
    name = models.CharField(max_length=30)
    university = models.CharField(max_length=100, null=True, blank=True)
    major = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    resume = models.FileField(max_length=100, blank=True,
                              upload_to=user_resume_path)

    # Additional fields for admin management
    status = models.CharField(
            max_length=20,
            choices=APP_STATUS_CHOICES,
            default=APP_STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def on_update_status(self):
        if self.status == OnlineApplication.APP_STATUS_PASS_RESUME:
            # if status --> YES, create a TestRequest & send link to candidate
            test_request = TestRequest.createTestRequestForApplication(self)
            send_test_request(test_request)
        elif self.status == OnlineApplication.APP_STATUS_FAIL_RESUME:
            send_reject(self)

    def save(self, *args, **kwargs):
        is_updated_status = False
        if self.pk is not None:
            # if its an updated record
            old_instance = OnlineApplication.objects.get(pk=self.pk)
            if self.status != old_instance.status:
                is_updated_status = True

        super(OnlineApplication, self).save(*args, **kwargs)
        if is_updated_status:
            self.on_update_status()


class TestRequest(models.Model):
    STATUS_NEW = "NEW"   # Test Request link is created but candidate haven't request
    STATUS_SET = "SET"   # Candidate set time, and test email not sent yet
    STATUS_SENT = "SENT" # Test email is sent
    STATUS_CHOICES = (
        (STATUS_NEW, "New"),
        (STATUS_SET, "Set"),
        (STATUS_SENT, "Sent"),
    )

    VER_ENGLISH = "EN"
    VER_CHINESE = "CN"
    VERSION_CHOICES = (
        (VER_ENGLISH, "English"),
        (VER_CHINESE, "Chinese"),
    )

    application = models.OneToOneField(
            'OnlineApplication',
            on_delete=models.CASCADE,
            related_name="test_request")
    hashstr = models.CharField(
            max_length=100,
            unique=True)
    version = models.CharField(
            max_length=10,
            choices=VERSION_CHOICES,
            default=VER_ENGLISH)
    date = models.DateField(
            null=True,
            blank=False)
    time = models.TimeField(
            null=True,
            blank=True,
            default=datetime.time(19,00))
    status = models.CharField(
            max_length=10,
            choices=STATUS_CHOICES,
            default=STATUS_NEW)

    # Additional fields for admin management
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.application.position, str(self.date))

    def get_absolute_url(self):
        return reverse('main.career.test', kwargs={'req_id': self.id, 'hashstr': self.hashstr})

    def get_date(self):
        if self.date:
            return self.date.strftime("%Y-%m-%d")
        else:
            return "-"

    def get_time(self):
        if self.time:
            return self.time.strftime("%H:%M")
        else:
            return "-"

    def get_datetime(self):
        return "{} {}".format(self.get_date(), self.get_time())

    @staticmethod
    def createTestRequestForApplication(application):
        try:
            test_request = application.test_request
            # already exist
            return test_request
        except ObjectDoesNotExist:
            test_request = TestRequest(
                    application=application,
                    hashstr=gen_hashstr(application.email))
            test_request.save()
            return test_request


class Position(object):

    def __init__(self, title, desc, qualification):
        """
        title: string
        desc: []
        qualification: []
        """
        self.title = title
        self.desc = desc
        self.qualification = qualification
