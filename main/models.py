from __future__ import unicode_literals

from django.db import models

class TestRequest(models.Model):
    DEVELOPER = "Dev"
    RESEARCHER = "Res"
    POSITION_CHOICES = (
        (DEVELOPER, "Developer"),
        (RESEARCHER, "Researcher"),
    )

    STATUS_SENT = "Sent"
    STATUS_PENDING = "Pend"
    STATUS_CHOICES = (
        (STATUS_SENT, "Sent"),
        (STATUS_PENDING, "Pending"),
    )

    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    name = models.CharField(max_length=30)
    university = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    # Additional fields for admin management
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

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

