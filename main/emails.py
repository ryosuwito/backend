# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template import loader, Context
from django.utils.html import strip_tags

from .models import get_test_filepath
from .types import (
    JobPosition,
    Workplace,
    JobType,
)


COMPANY_CAREER_EMAIL = settings.COMPANY_CAREER_EMAIL
SENDER = settings.SEND_EMAIL_FROM


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
        subject="Job application - {}".format(application.get_position_display),
        email_template="main/email_apply_confirm.html",
        email_context={
            'name': application.name,
            'position': application.get_position_display,
        },
        recipients=[application.email, ],
        cc=[COMPANY_CAREER_EMAIL]
    )


def send_online_application_summary(application):
    """
    forward candidate application to company career email
    """
    subject = "Job application - {}_{}_{}".format(
        application.get_position_display,
        JobType[application.typ].value,
        Workplace[application.workplace].value,
    )

    send_templated_email(
        subject=subject,
        email_template="main/email_apply_summary.html",
        email_context={'application': application},
        recipients=[COMPANY_CAREER_EMAIL, ],
        files=application.resume.path)


def send_test_request(test_request):
    """
    send email to applicants with test request link for them to schedule test
    """
    template = "main/email_test_request.html"

    send_templated_email(
        subject="test scheduling: {}"
                .format(test_request.application.get_position_display),
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
        if not test_request.application.is_intern:
            email_template = "main/email_test_research.html"
        else:
            email_template = "main/email_test_intern_researcher.html"
    elif test_request.application.position in [
            JobPosition.DATA_ENGINEER.name,
            JobPosition.OP_SPECIALIST.name]:
        email_template = "main/email_test_data_engineer.html"
    elif test_request.application.is_role_dev():
        email_template = "main/email_test_dev.html"
    elif test_request.application.is_role_dev() and test_request.application.is_intern:
        email_template = "main/email_test_dev.html"
    else:
        raise ValueError("Invalid position")

    file_test = get_test_filepath(test_request)
    assert (os.path.isfile(file_test))

    send_templated_email(
        subject="written test: {}"
                .format(test_request.application.get_position_display),
        email_template=email_template,
        email_context={
            'name': test_request.application.name},
        recipients=[test_request.application.email, ],
        cc=[COMPANY_CAREER_EMAIL],
        files=file_test)


def send_reminding_test_email(req, minutes, online_test_host):
    send_templated_email(
        subject="Dynamic Technology Lab test/project will start in under {} minutes".format(minutes),
        email_template="main/email_reminding_test.html",
        email_context={
            'req': req, 'minutes': minutes, 'online_test_host': online_test_host,
        },
        recipients=[req.application.email],
        cc=[COMPANY_CAREER_EMAIL],
    )


def send_token_email(context):
    """
    send token to candidate on scheduled datetime
    """
    email_template = 'main/email_online_test_access.html'
    test_request = context['test_request']

    send_templated_email(
        subject="Dynamic Technology Lab written test/project: {}"
                .format(test_request.application.get_position_display),
        email_template=email_template,
        email_context=context,
        recipients=[test_request.application.email, ],
        cc=[COMPANY_CAREER_EMAIL],)


def send_campaign_passed_resume_email(context):
    """
    send campaign passed_resume to candidate on scheduled datetime
    """
    email_template = 'recruitment_campaign/passed_resume_email.html'
    campaign_application = context['campaign_application']
    campaign = context['campaign']

    send_templated_email(
        subject="Dynamic Technology Lab - Successful registration for %s" % campaign.name,
        email_template=email_template,
        email_context=context,
        recipients=[campaign_application.application.email,],
        cc=[COMPANY_CAREER_EMAIL],)


def send_invitation_to_attend_recuitment_campaign(context):
    """
    send invitation to people who have applied to attend the coming recruitment campaign
    """
    email_template = 'recruitment_campaign/invitation_email.html'
    application = context['application']

    send_templated_email(
        subject="Dynamic Technology Lab Invitation",
        email_template=email_template,
        email_context=context,
        recipients=[application.email, ],
        cc=[COMPANY_CAREER_EMAIL],)


def send_on_token_failed(application):
    """
    """
    body = "Fail to send token to candidate {} with application id {}".format(application.name, application.id)
    send_mail(body, body, SENDER, recipient_list=[COMPANY_CAREER_EMAIL], fail_silently=True)


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
