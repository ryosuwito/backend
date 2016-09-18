from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from main.hashes import gen_hashstr
from main.emails import send_test_request
import datetime


class OnlineApplication(models.Model):
    DEVELOPER = "Dev"
    Q_RESEARCHER = "QRes"
    FQ_RESEARCHER = "FQRes"
    POSITION_CHOICES = (
        (DEVELOPER, "Developer"),
        (Q_RESEARCHER, "Quantitative Researcher"),
        (FQ_RESEARCHER, "Fundamental Quantitative Researcher"),
    )

    APP_STATUS_NEW = "New"
    APP_STATUS_YES = "Yes"
    APP_STATUS_NO = "No"
    APP_STATUS_CHOICES = (
        (APP_STATUS_NEW, "New"),
        (APP_STATUS_YES, "Yes"),
        (APP_STATUS_NO, "No")
    )


    position = models.CharField(
            max_length=10,
            choices=POSITION_CHOICES,
            default=DEVELOPER)
    name = models.CharField(max_length=30)
    university = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    resume = models.CharField(max_length=100) # resume file name

    # Additional fields for admin management
    status = models.CharField(
            max_length=10,
            choices=APP_STATUS_CHOICES,
            default=APP_STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def on_update_status(self):
        if self.status == OnlineApplication.APP_STATUS_YES:
            # if status: NEW --> YES, create a TestRequest & send link to candidate
            test_request = TestRequest.createTestRequestForApplication(self)
            send_test_request(test_request)

    def save(self, *args, **kwargs):
        is_updated_status = False
        if self.pk is not None:
            # if its an updated record
            old_instance = OnlineApplication.objects.get(pk=self.pk)
            if old_instance.status == OnlineApplication.APP_STATUS_NEW:
                if self.status != old_instance.status:
                    is_updated_status = True

        super(OnlineApplication, self).save(*args, **kwargs)
        if is_updated_status:
            on_update_status()



class TestRequest(models.Model):
    STATUS_NEW = "New"         # Test Request link is created but candidate haven't request
    STATUS_PENDING = "Pending" # Test Request is created but email is not sent
    STATUS_SENT = "Sent"       # email is sent
    STATUS_CHOICES = (
        (STATUS_NEW, "New"),
        (STATUS_PENDING, "Pending"),
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

