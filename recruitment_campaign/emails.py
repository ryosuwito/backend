# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context
from django.utils.html import strip_tags


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
        email_template="emails/email_apply_confirm.html",
        email_context={
            'application': application
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
        application.get_type_display,
        application.get_workplace_display,
    )

    send_templated_email(
        subject=subject,
        email_template="emails/email_apply_summary.html",
        email_context={'application': application},
        recipients=[COMPANY_CAREER_EMAIL, ],
        files=application.resume.path)
