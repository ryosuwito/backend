# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta

from django.utils import timezone
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from .hashes import gen_hashstr


def user_resume_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/resumes/{email}_filename
    return 'resumes/{}_{}'.format(instance.email, filename)


def get_test_filepath(test_request, version=None):
    from django.conf import settings
    if version is None:
        version = test_request.version
    return settings.TEST_FILES.get(test_request.application.position, {}).get(version)


class OnlineApplication(models.Model):
    DEVELOPER = "DEV"
    DATA_ENGINEER = 'DATA_ENGINEER'
    OPERATION_SPECIALIST = 'OP_SPECIALIST'
    Q_RESEARCHER = "QRES"
    FQ_RESEARCHER = "FQRES"
    INTERN_Q_RESEARCHER = 'INTERN_QRES'
    POSITION_CHOICES = (
        (DEVELOPER, "Developer"),
        (DATA_ENGINEER, "Data Engineer"),
        (OPERATION_SPECIALIST, "Operation Specialist"),
        (Q_RESEARCHER, "Quantitative Researcher"),
        (FQ_RESEARCHER, "Fundamental Quantitative Researcher"),
    )
    INTERN_POSITION_CHOICES = (
        (INTERN_Q_RESEARCHER, "Quantitative Researcher (Intern)"),
    )

    APP_STATUS_NEW = "NEW"
    APP_STATUS_PASS_RESUME = "PASS_RESUME"
    APP_STATUS_FAIL_RESUME = "FAIL_RESUME"
    APP_STATUS_PASS_TEST = "PASS_TEST"
    APP_STATUS_FAIL_TEST = "FAIL_TEST"
    APP_STATUS_DOES_NOT_FINISH_TEST = 'DNF_TEST'
    APP_STATUS_CHOICES = (
        (APP_STATUS_NEW, "NEW"),
        (APP_STATUS_PASS_RESUME, "PASS RESUME"),
        (APP_STATUS_FAIL_RESUME, "FAIL RESUME"),
        (APP_STATUS_PASS_TEST, "PASS TEST"),
        (APP_STATUS_FAIL_TEST, "FAIL TEST"),
        (APP_STATUS_DOES_NOT_FINISH_TEST, "DNF TEST"),
    )

    position = models.CharField(
        max_length=20,
        choices=(POSITION_CHOICES + INTERN_POSITION_CHOICES),
        default=DEVELOPER)
    name = models.CharField(max_length=30)
    university = models.CharField(max_length=100, null=True, blank=True)
    school = models.CharField(max_length=200, null=True, blank=True)
    major = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    resume = models.FileField(max_length=100, blank=True,
                              upload_to=user_resume_path)
    info_src = models.CharField(max_length=200, null=False, blank=False, default="N.A")

    # Additional fields for admin management
    status = models.CharField(
        max_length=20,
        choices=APP_STATUS_CHOICES,
        default=APP_STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.email

    def is_role_dev(self):
        return self.position in [OnlineApplication.DEVELOPER]

    def is_role_researcher(self):
        return self.position in [OnlineApplication.Q_RESEARCHER,
                                 OnlineApplication.FQ_RESEARCHER]

    def is_role_intern(self):
        return self.position == OnlineApplication.INTERN_Q_RESEARCHER

    def is_role_data_engine(self):
        return self.position == OnlineApplication.DATA_ENGINEER

    def is_role_operation(self):
        return self.position == OnlineApplication.OPERATION_SPECIALIST

    def on_update_status(self):
        from .emails import send_test_request, send_reject
        if self.status == OnlineApplication.APP_STATUS_PASS_RESUME:
            # if status --> PASS_RESUME, create a TestRequest & send link to candidate
            test_request = TestRequest.createTestRequestForApplication(self)
            send_test_request(test_request)
        elif self.status in [
                OnlineApplication.APP_STATUS_FAIL_RESUME,
                OnlineApplication.APP_STATUS_FAIL_TEST]:
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
    STATUS_NEW = "NEW"    # Test Request link is created but candidate haven't request
    STATUS_SET = "SET"    # Candidate set time, and test email not sent yet
    STATUS_SENT = "SENT"  # Test email is sent
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
    datetime = models.DateTimeField(
        null=True,
        blank=False)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_NEW)

    # Additional fields for admin management
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{}-{}-{}".format(self.application.email, self.application.position, self.datetime)

    def get_absolute_url(self):
        return reverse('main.career.test', kwargs={'req_id': self.id, 'hashstr': self.hashstr})

    def get_datetime(self):
        if self.datetime:
            return self.datetime
        else:
            return '-'

    def allow_update(self):
        # allow update up to 2 days prior scheduled date
        if self.status == TestRequest.STATUS_NEW:
            return True
        if self.status == TestRequest.STATUS_SENT:
            return False
        if self.status == TestRequest.STATUS_SET:
            return (timezone.now() + timedelta(days=2)) <= self.datetime

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


class InternCandidate(models.Model):
    chinese_name = models.CharField(max_length=30)
    english_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, unique=True)

    def __unicode__(self):
        return u"{}: {}({})".format(self.email, self.chinese_name, self.english_name)


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
