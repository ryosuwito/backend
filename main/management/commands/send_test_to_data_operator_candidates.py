from django.core.management.base import BaseCommand
from django.conf import settings

from main.models import OnlineApplication
from main import (
    types,
    emails,
)


class Command(BaseCommand):
    help = 'Send email to condidates for the data operator position'

    def handle(self, *args, **options):
        online_applications = OnlineApplication.objects.filter(
            position=types.JobPosition.DATA_OPERATOR.name,
            status=OnlineApplication.APP_STATUS_NEW,
        )
        subject = 'Dynamic Technology Lab - Data Operator Test'
        for app in online_applications:
            emails.send_templated_email(
                subject=subject,
                email_template='main/data_operator_test.html',
                email_context={'app': app},
                sender='Dynamic Technology Lab Career <{}>'.format(emails.COMPANY_CAREER_EMAIL),
                recipients=[app.email],
                cc=[emails.COMPANY_CAREER_EMAIL],
                files=settings.DATA_OPERATOR_ATTACHMENTS,
            )
            OnlineApplication.objects.filter(id=app.id).update(status=OnlineApplication.APP_STATUS_OTHER)
            self.stdout.write(
                self.style.SUCCESS('The email for the data operator test has been sent to {}'.format(app.email)))
