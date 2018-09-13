# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context
from django.utils.html import strip_tags

from .models import get_test_filepath, OnlineApplication


COMPANY_CAREER_EMAIL = settings.COMPANY_CAREER_EMAIL
SENDER = COMPANY_CAREER_EMAIL


def send_templated_email(subject, email_template, email_context,
                         recipients, sender=SENDER, cc=None, bcc=None,
                         fail_silently=True, files=None):
    c = Context(email_context)
    template = loader.get_template(email_template)
    text = strip_tags(template.render(c))
    html = template.render(c)
    message = EmailMultiAlternatives(
        subject,
        text,
        sender,
        recipients,
        cc=cc,
        bcc=bcc)
    message.attach_alternative(html, "text/html")
    if files:
        if type(files) != list:
            files = [files, ]
        for f in files:
            message.attach_file(f)

    return message.send(fail_silently)


def send_online_application_confirm(application):
    """
    send email to applicants indicating the application is received
    """
    send_templated_email(
        subject="job application - {}".format(application.get_position_display()),
        email_template="main/email_apply_confirm.html",
        email_context={
            'name': application.name,
            'position': application.get_position_display()
        },
        recipients=[application.email, ],
        cc=[COMPANY_CAREER_EMAIL]
    )


def send_online_application_summary(application):
    """
    forward candidate application to company career email
    """
    send_templated_email(
        subject="job application - {}".format(application.get_position_display()),
        email_template="main/email_apply_summary.html",
        email_context={'application': application},
        recipients=[COMPANY_CAREER_EMAIL, ],
        files=application.resume.path)


def send_test_request(test_request):
    """
    send email to applicants with test request link for them to schedule test
    """
    template = "main/email_test_request.html"

    if test_request.application.position in [
            OnlineApplication.DATA_ENGINEER,
            OnlineApplication.OPERATION_SPECIALIST,
            OnlineApplication.INTERN_DATA_ENGINEER]:
        template = "main/email_test_request_for_data_engineer.html"

    send_templated_email(
        subject="test scheduling: {}"
                .format(test_request.application.get_position_display()),
        email_template=template,
        email_context={
            'name': test_request.application.name,
            'req': test_request},
        recipients=[test_request.application.email, ],
        cc=[COMPANY_CAREER_EMAIL]
    )


def send_test(test_request):
    """
    send test file to candidate on scheduled datetime
    """
    if test_request.application.is_role_researcher():
        email_template = "main/email_test_research.html"
    elif test_request.application.position == OnlineApplication.INTERN_Q_RESEARCHER:
        email_template = "main/email_test_intern_researcher.html"
    elif test_request.application.position in [
            OnlineApplication.DATA_ENGINEER,
            OnlineApplication.OPERATION_SPECIALIST,
            OnlineApplication.INTERN_DATA_ENGINEER]:
        email_template = "main/email_test_data_engineer.html"
    elif test_request.application.is_role_dev():
        email_template = "main/email_test_dev.html"
    else:
        raise ValueError("Invalid position")

    file_test = get_test_filepath(test_request)
    assert (os.path.isfile(file_test))

    send_templated_email(
        subject="written test: {}"
                .format(test_request.application.get_position_display()),
        email_template=email_template,
        email_context={
            'name': test_request.application.name},
        recipients=[test_request.application.email, ],
        cc=[COMPANY_CAREER_EMAIL],
        files=file_test)


def send_reject(application):
    """
    send reject email to candidate.
    """
    send_templated_email(
        subject="dtl job opportunity",
        email_template="main/email_reject.html",
        email_context={
            'name': application.name,
        },
        recipients=[application.email, ],
        cc=[COMPANY_CAREER_EMAIL]
    )
