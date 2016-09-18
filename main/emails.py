from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context
from django.utils.html import strip_tags


def send_templated_email(subject, email_template_name, email_context, recipients,
                         sender=None, cc=None, bcc=None, fail_silently=True, files=None):
    print "send templated email!"
    c = Context(email_context)
    template = loader.get_template(email_template_name)
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
            files = [files,]
        for f in files:
            message.attach_file(f)

    return message.send(fail_silently)


def send_online_application_summary(application, resume):
    """
    forward application form to careers@dytechlab.com
    """
    send_templated_email(
            subject="DTL online application",
            email_template_name="main/email_apply_summary.html",
            email_context={},
            recipients=['ynguyen@dytechlab.com',],
            files=resume)

def send_online_application_confirm(application):
    """
    send email to applicants indicating the application is received
    """
    send_templated_email(
            subject="DTL Career Online Application",
            email_template_name="main/email_apply_confirm.html",
            email_context={'name': application.name},
            recipients=[application.email, ])


def send_test_request(test_request):
    """
    send email to applicants with test request link for them to schedule test
    """
    from main.models import OnlineApplication
    send_templated_email(
            subject="DTL Schedule Test Online",
            email_template_name="main/email_test_request.html",
            email_context={
                'name': test_request.application.name,
                'req': test_request
            },
            recipients=[test_request.application.email, ])


def send_test(test_request):
    """
    send test file to candidate on scheduled datetime
    """
    send_templated_email(
            subject="DTL Test",
            email_template_name="main/email_test.html",
            email_context={},
            recipients=[test_request.application.email, ],
            files="")
