# -*- coding: utf-8 -*-
import logging
import jwt
import time as _time
import datetime

from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages

from main.emails import send_campaign_passed_resume_email

from django.contrib import admin
from .models import (
    Campaign,
    CampaignApplication,
)

from .forms import (
    CampaignApplicationAdminForm,
)

from main.models import TestRequest
from main import cron


logger = logging.getLogger(__name__)
TOKEN_SENT = 'TOKEN_SENT'
TOKEN_SEND_FAILED = 'TOKEN_SEND_FAILED'
_EPOCH = datetime.datetime(1970, 1, 1, tzinfo=timezone.utc)


def timestamp(dtime):
    "Return POSIX timestamp as float"
    if dtime.tzinfo is None:
        return _time.mktime((dtime.year, dtime.month, dtime.day,
                             dtime.hour, dtime.minute, dtime.second,
                             -1, -1, -1)) + dtime.microsecond / 1e6
    else:
        return (dtime - _EPOCH).total_seconds()


StatusType = CampaignApplication.StatusType


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'active', 'starttime', 'test_id')
    list_display_links = ('id', 'name')
    list_filter = ('name',)


@admin.register(CampaignApplication)
class ApplicationAdmin(admin.ModelAdmin):
    form = CampaignApplicationAdminForm
    actions = ['pass_resume_selected_applications']

    def pass_resume_selected_applications(self, request, queryset):
        """
        Sep 2020 event - all candidates will do the test at a specific time
        """
        success_app_cnt = 0
        error_app_cnt = 0
        for campaign_app in queryset.filter(status=StatusType.new.value):
            app = campaign_app.application
            test_request = TestRequest.createTestRequestForApplication(app)
            try:
                campaign = campaign_app.campaign
                payload = {
                    'username': get_random_string(15),
                    'password': get_random_string(15),
                    'timestamp': timestamp(timezone.now()),
                    'start_time_timestamp': timestamp(campaign.starttime),
                    'fullname': app.name,
                    'test_id': campaign.test_id,
                    'email': app.email,
                }
                token = jwt.encode(payload, settings.SHARE_KEY, 'HS256')
                # Set token status failed anyway to avoid resend.
                test_request.token = token
                test_request.token_status = cron.TOKEN_READY
                test_request.status = TestRequest.STATUS_SET
                test_request.datetime = campaign.starttime
                test_request.save(update_fields=('token', 'token_status', 'status', 'datetime'))
                CampaignApplication.objects\
                    .filter(id=campaign_app.id)\
                    .update(status=StatusType.passed_resume.value)

                context = {
                    'campaign': campaign,
                    'campaign_application': campaign_app,
                    'application': app,
                }
                send_campaign_passed_resume_email(context)
                success_app_cnt += 1
            except Exception as err:
                test_request.refresh_from_db()
                test_request.token_status = TOKEN_SEND_FAILED
                test_request.note = str(err)
                test_request.save(update_fields=('token_status', 'note'))
                CampaignApplication.objects\
                    .filter(id=campaign_app.id)\
                    .update(status=StatusType.FAIL_TO_PASS_RESUME.value)
                error_app_cnt += 1

        if success_app_cnt > 0:
            self.message_user(request, "%d applications was successfully passed" % success_app_cnt, messages.SUCCESS)

        if error_app_cnt > 0:
            self.message_user(request, "%d applications was failed to pass" % error_app_cnt, messages.ERROR)

    def campaign_name(self, obj):
        return obj.campaign.name

    def position(self, obj):
        return obj.application.position

    def name(self, obj):
        return obj.application.name

    def email(self, obj):
        return obj.application.email

    def university(self, obj):
        return obj.application.university

    def school(self, obj):
        return obj.application.school

    def major(self, obj):
        return obj.application.major

    list_display = (
        'id',
        'campaign_name',
        'position',
        'name',
        'email',
        'university',
        'school',
        'major',
        'status',
    )
    list_select_related = ('campaign', 'application')
    list_display_links = ('id', 'name')
    list_filter = ('campaign__name', 'application__position', 'status')
