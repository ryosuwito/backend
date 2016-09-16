from __future__ import unicode_literals

from django.db import models


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
    # TODO: create a pre-save signals
    # If status: New -> Yes, create a TestRequest instance & send link to candidate


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
    signature = models.CharField(max_length=100, unique=True)
    version = models.CharField(
            max_length=10,
            choices=VERSION_CHOICES,
            default=VER_ENGLISH)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
            max_length=10,
            choices=STATUS_CHOICES,
            default=STATUS_NEW)
    # Additional fields for admin management
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return "{} {}".format(self.application.position, str(self.date)) 

    def get_date(self):
        return self.date.strftime("%Y-%m-%d")

    def get_time(self):
        return self.time.strftime("%H:%M")

    def get_datetime(self):
        return "{} {}".format(self.get_date(), self.get_time())

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

