import os
from django.core.management.base import BaseCommand
from main.models import InternCandidate


class Command(BaseCommand):
    help = 'Import intern candicate from csv file, old records will be removed'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='?', type=str)

    def handle(self, *args, **options):
        # TODO: make this function a db transaction
        csv_file = options['csv_file']
        assert(os.path.isfile(csv_file))

        intern_list = []

        with open(csv_file, 'r') as f:
            f.readline() # skip header
            # header: chinese_name, english_name, email
            for line in f:
                chinese_name, english_name, email = line.strip().decode('utf-8').split(',')
                chinese_name = chinese_name.strip()
                english_name = english_name.strip()
                email = email.strip()
                intern_list.append(InternCandidate(
                    chinese_name=chinese_name,
                    english_name=english_name,
                    email=email))
        # Replace db
        InternCandidate.objects.all().delete()
        for candidate in intern_list:
            candidate.save()

        assert(InternCandidate.objects.count() == len(intern_list))
        print 'Imported {} candidates'.format(len(intern_list))
