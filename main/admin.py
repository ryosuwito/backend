# -*- coding: utf-8 -*-
from django.contrib import admin
from main.models import OnlineApplication, TestRequest, InternCandidate
from main.forms import OnlineApplicationForm
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

    get_scheduled_test.short_description = "Scheduled Test"
    list_display = ('name', 'university', 'school', 'major', 'email',
                    'position', 'status', get_scheduled_test, 'info_src',
                    'is_onsite_recruiment', 'test_site',)
    list_editable = ('status', 'is_onsite_recruiment',)
    list_filter = ('position', 'status', 'is_onsite_recruiment', 'test_site',)


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
    list_filter=('application__position', 'application__test_site',)



@admin.register(InternCandidate)
class InternCandidateAdmin(admin.ModelAdmin):
    list_display = ('email', 'chinese_name', 'english_name',)
    pass
