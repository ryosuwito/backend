from django.core.management.base import BaseCommand

from main.models import OpenJob
from main import types


class Command(BaseCommand):
    help = 'Add all possible open jobs'

    def handle(self, *args, **options):
        for position in types.JobPosition:
            for typ in types.JobType:
                for wp in types.Workplace:
                    msg = 'OpenJob ({}, {}, {})'.format(position.name, typ.name, wp.name)
                    open_job_prop = {
                        'position': position.name,
                        'typ': typ.name,
                        'workplace': wp.name,
                    }
                    try:
                        open_job = OpenJob(**open_job_prop)
                        open_job.save()
                    except Exception as err:
                        self.stdout.write(self.style.ERROR(err))
                    else:
                        msg = (' ').join([msg, 'has just added successfully!'])
                        self.stdout.write(self.style.SUCCESS(msg))
