# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta

from django.utils import timezone
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from .hashes import gen_hashstr
from .types import (
    JobPosition,
    JobType,
    Workplace,
    JobTypeChoices,
    JobWorkplaceChoices,
    JobPositionChoices,
)


def user_resume_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/resumes/{email}_filename
    return "resumes/{}_{}".format(instance.email, filename)


def get_test_filepath(test_request, version=None):
    from django.conf import settings
    if version is None:
        version = test_request.version
    return settings.TEST_FILES.get(test_request.application.position, {}).get(version)


class OnlineApplication(models.Model):
    APP_STATUS_NEW = "NEW"
    APP_STATUS_PASS_RESUME = "PASS_RESUME"
    APP_STATUS_FAIL_RESUME = "FAIL_RESUME"
    APP_STATUS_PASS_TEST = "PASS_TEST"
    APP_STATUS_FAIL_TEST = "FAIL_TEST"
    APP_STATUS_DOES_NOT_FINISH_TEST = "DNF_TEST"
    APP_STATUS_CHOICES = (
        (APP_STATUS_NEW, "NEW"),
        (APP_STATUS_PASS_RESUME, "PASS RESUME"),
        (APP_STATUS_FAIL_RESUME, "FAIL RESUME"),
        (APP_STATUS_PASS_TEST, "PASS TEST"),
        (APP_STATUS_FAIL_TEST, "FAIL TEST"),
        (APP_STATUS_DOES_NOT_FINISH_TEST, "DNF TEST"),
    )

    typ = models.CharField(max_length=255, default=JobType.FULLTIME_JOB.name)
    workplace = models.CharField(max_length=255, default=Workplace.SINGAPORE.name)
    position = models.CharField(max_length=255,default=JobPosition.DEV.value)

    name = models.CharField(max_length=30)
    university = models.CharField(max_length=100, null=True, blank=True)
    school = models.CharField(max_length=200, null=True, blank=True)
    major = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    resume = models.FileField(max_length=100, blank=True,
                              upload_to=user_resume_path)
    info_src = models.CharField(max_length=200, null=False, blank=False, default="N.A")

    start_time = models.DateField(max_length=255, blank=True, null=True)

    # Additional fields for admin management
    status = models.CharField(
        max_length=20,
        choices=APP_STATUS_CHOICES,
        default=APP_STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    # if the application is for onsite event
    is_onsite_recruiment = models.BooleanField(default=False, blank=True, null=False)
    test_site = models.CharField(max_length=50, null=True, blank=True)

    @property
    def get_position_display(self):
        obj_prop_value = getattr(self, 'position', '')
        enum_value = getattr(JobPosition, obj_prop_value, None)
        return obj_prop_value if enum_value is None else enum_value.value

    def __unicode__(self):
        return self.email

    def is_role_dev(self):
        return self.position in [JobPosition.DEV.name]

    def is_role_researcher(self):
        return self.position in [JobPosition.QRES.name,
                                 JobPosition.FQRES.name]

    @property
    def is_intern(self):
        return 'intern' in self.typ.lower()

    @property
    def from_china_event(self):
        return self.is_onsite_recruiment

    def on_update_status(self):
        # TODO: logics should not put in models
        from .emails import send_test_request
        if self.status == OnlineApplication.APP_STATUS_PASS_RESUME:
            # if status --> PASS_RESUME, create a TestRequest & send link to candidate
            test_request = TestRequest.createTestRequestForApplication(self)
            send_test_request(test_request)
        elif self.status in [
                OnlineApplication.APP_STATUS_FAIL_RESUME,
                OnlineApplication.APP_STATUS_FAIL_TEST]:
            # send_reject(self)
            # Dont send reject email for now !
            pass

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
    STATUS_NEW = "NEW"    # Test Request link is created but candidate haven"t request
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
        "OnlineApplication",
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
    token_status = models.CharField(
        max_length=255, blank=True, null=True, default=None)
    token = models.TextField(
        null=True, default='', blank=True)

    # Additional fields for admin management
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{}-{}-{}".format(self.application.email, self.application.position, self.datetime)

    def get_absolute_url(self):
        return reverse(
            "main.career.test",
            kwargs={"req_id": self.id, "hashstr": self.hashstr}
        )

    def get_onsite_absolute_url(self):
        return reverse(
            "chinaevent.register",
            kwargs={"req_id": self.id, "hashstr": self.hashstr}
        )

    def get_datetime(self):
        if self.datetime:
            return self.datetime
        else:
            return "-"

    def allow_update(self):
        # allow update up to 2 days prior scheduled date
        if self.status == TestRequest.STATUS_NEW:
            return True
        if self.status == TestRequest.STATUS_SENT:
            return False
        if self.status == TestRequest.STATUS_SET:
            return (timezone.now() + timedelta(days=2)) <= self.datetime

    @property
    def test_site(self):
        return self.application.test_site

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
    def __init__(self, title, symbol, desc, qualification,
                 location=None, duration=None, plus=None):
        """
        title: string
        desc: []
        qualification: []
        """
        self.title = title
        self.symbol = symbol
        self.desc = desc
        self.qualification = qualification
        self.location = location
        self.duration = duration
        self.plus = plus


class OpenJob(models.Model):
    position = models.CharField(max_length=255, choices=JobPositionChoices)
    typ = models.CharField(max_length=255, choices=JobTypeChoices)
    workplace = models.CharField(max_length=255, choices=JobWorkplaceChoices)
    active = models.BooleanField(default=True, blank=True, null=False)
    test_id = models.CharField(max_length=255, null=True, default=None, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = [
            ('position',),
            ('position', 'typ'),
        ]
        unique_together = [
            ('position', 'typ', 'workplace')
        ]
