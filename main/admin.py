# -*- coding: utf-8 -*-
import datetime

from django.contrib import admin
from main.models import OnlineApplication, TestRequest, InternCandidate, OpenJob
from main.types import JobType
from django.core.exceptions import ObjectDoesNotExist


@admin.register(OnlineApplication)
class OnlineApplicationAdmin(admin.ModelAdmin):
    def get_scheduled_test(application):
        if application.status == OnlineApplication.APP_STATUS_FAIL_RESUME:
            return "Not Applicable"
        elif application.status == OnlineApplication.APP_STATUS_PASS_RESUME:
            try:
                return application.test_request.get_datetime()
            except ObjectDoesNotExist:
                return "Oops no test request!"
        else:
            return "None"

    def start_and_end_time(obj):
        start_time = obj.start_time
        if start_time is None:
            return "---"

        if obj.typ == JobType.FULLTIME_INTERNSHIP.name:
            end_time = start_time + datetime.timedelta(days=90) # 3 months after start working day
        elif obj.typ == JobType.PARTTIME_INTERNSHIP.name:
            end_time = start_time + datetime.timedelta(days=120) # 4 months after start working day
        else:
            end_time = None

        start_time = start_time.strftime('%Y.%m.%d')
        end_time = 'oo' if end_time is None else end_time.strftime('%Y.%m.%d')

        return '{}-{}'.format(start_time, end_time)

    get_scheduled_test.short_description = "Scheduled Test"
    list_display = ('name', 'university', 'school', 'major', 'email',
                    'position', 'typ', 'workplace', start_and_end_time, 'status', get_scheduled_test, 'info_src',
                    'is_onsite_recruiment', 'test_site',)
    list_editable = ('status', 'is_onsite_recruiment',)
    list_filter = ('typ', 'workplace', 'position', 'status', 'is_onsite_recruiment', 'test_site',)


@admin.register(TestRequest)
class TestRequestAdmin(admin.ModelAdmin):
    def get_position(obj):
        if not obj.application:
            return 'NO APPLICATION FOUND'
        return obj.application.position

    get_position.short_description = 'Position'

    list_display = ('application', get_position, 'get_absolute_url',
                    'version', 'get_datetime', 'status')
    list_selected_related = ('application')
    list_display_links = ('application',)
    list_filter = ('application__position', 'application__test_site',)


@admin.register(InternCandidate)
class InternCandidateAdmin(admin.ModelAdmin):
    list_display = ('email', 'chinese_name', 'english_name',)
    pass


@admin.register(OpenJob)
class OpenJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'typ', 'workplace', 'position')
    list_display_links = ('id',)
