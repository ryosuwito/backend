# -*- coding: utf-8 -*-
import logging
import jwt
import time as _time
import datetime
import json
import uuid
import requests

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages

from main.emails import send_campaign_passed_resume_email

from recruitment_campaign import emails as campaign_emails

from django.contrib import admin

from .models import (
    Campaign,
    GroupCampaign,
    CampaignApplication,
    CampaignOnlineApplication,
    ApplicationStatus,
    EventLog,
    GroupApplication,
    IndividualApplicant
)
from .forms import (
    CampaignApplicationAdminForm,
)
from .types import ApplicationStatus2021

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


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'data')
    list_display = ('name',)
    list_display_links = ('name',)
    list_filter = ('name',)


@admin.register(CampaignOnlineApplication)
class CampaignOnlineApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'position',
        'name',
        'email',
        'university',
        'school',
        'major',
        'status',
        'info_src',
    )
    list_display_links = ('id', 'name')
    list_filter = ('position', 'status', 'created_at')
    actions = [
        # 'pass_resume_selected_applications',
        # 'fail_selected_applications',
        'pass_resume_2021',
        'fail_resume_2021',
    ]

    def fail_selected_applications(self, request, queryset):
        app_len = len(queryset)
        updated_cnt = queryset\
            .filter(status=ApplicationStatus.NEW.name)\
            .update(status=ApplicationStatus.FAIL_RESUME.name)

        if updated_cnt > 0:
            self.message_user(
                request,
                "You have succefully failed %d applications" % updated_cnt,
                messages.SUCCESS
            )

        if app_len > updated_cnt:
            self.message_user(
                request,
                "There %d applications that were not new" % (app_len - updated_cnt),
                messages.ERROR
            )

    def fail_resume_2021(self, request, queryset):
        self.fail_selected_applications(request, queryset)

    def pass_resume_2021(self, request, queryset):
        """
        """
        success_app_cnt = 0
        error_app_cnt = 0
        campaigns = Campaign.objects.filter(active=True)
        campaign_cnt = len(campaigns)
        if campaign_cnt != 1:
            self.message_user(
                request,
                "It needs exactly one active campaign to pass resumes, there were %d of them" % campaign_cnt, messages.ERROR  # NoQA
            )
            return

        campaign = campaigns.get()
        tests_data = {}
        try:
            campaign_data = json.loads(campaign.meta_data)
            for position in campaign_data['position']:
                test_info = campaign_data['test'][position]
                tests_data[position] = {
                    "time": parse_datetime(test_info['time']),
                    "test_id": test_info['test_id'],
                    "duration": test_info['duration']
                }
        except Exception as err:
            self.message_user(request, "Cannot parse campaign data", messages.ERROR)
            return

        for app in queryset.filter(status=ApplicationStatus.NEW.name):
            try:
                token = str(uuid.uuid4())
                payload = {
                    'username': get_random_string(15),
                    'password': get_random_string(15),
                    'timestamp': cron.timestamp(timezone.now()),
                    'start_time_timestamp': cron.timestamp(tests_data[app.position]['time']),
                    'fullname': app.name,
                    'test_id': tests_data[app.position]['test_id'],
                    'email': app.email,
                }
                jwt_token = jwt.encode(payload, settings.SHARE_KEY, 'HS256')
                event_log_data = {
                    'test': campaign_data['test'][app.position],
                    'token': token,
                    'payload': payload,
                    'jwt_token': jwt_token,
                }
                event_log = EventLog(
                    name="campaign_%d_application_%d_status_%s" % (campaign.id, app.id, ApplicationStatus2021.INVITE_SENT.name),  # NoQA
                    data=json.dumps(event_log_data)
                )
                event_log.save()
                create_token_event_data = {
                    'campaign': campaign.id,
                    'application': app.id,
                    'token_event_id': event_log.id,
                }
                EventLog.objects.create(name=token, data=json.dumps(create_token_event_data))
                CampaignOnlineApplication.objects\
                    .filter(id=app.id)\
                    .update(status=ApplicationStatus2021.INVITE_SENT.name)

                date = tests_data[app.position]['time'].strftime('%A, %d %B %Y')
                starttime = tests_data[app.position]['time'].strftime('%H:%M:%S')
                duration = tests_data[app.position]['duration']

                campaign_emails.send_invite_email_2021(campaign, app, date, starttime, duration, token)
                # Activate account here
                url = settings.ONLINE_TEST_ACTIVE_USER_LINK(jwt_token)
                res = requests.get(url)
                if res.status_code not in [200, 302]:
                    campaign_emails.send_on_token_failed(app)
                    logger.error('Cannot activate token for application {}'.format(app.id))
                    raise Exception('cannot_activate_token')

                success_app_cnt += 1
            except Exception as err:
                event_log = EventLog(
                    name="campaign_%d_application_%d_status_%s" % (campaign.id, app.id, ApplicationStatus2021.FAILED.name),  # NoQA
                    data=str(err)
                )
                event_log.save()
                CampaignOnlineApplication.objects\
                    .filter(id=app.id)\
                    .update(status=ApplicationStatus.PASS_RESUME_FAILED.name)
                error_app_cnt += 1

        if success_app_cnt > 0:
            self.message_user(request, "%d applications was successfully passed" % success_app_cnt, messages.SUCCESS)

        if error_app_cnt > 0:
            self.message_user(request, "%d applications was failed to pass" % error_app_cnt, messages.ERROR)


# @admin.register(CampaignApplication)
class ApplicationAdmin(admin.ModelAdmin):
    form = CampaignApplicationAdminForm
    actions = [
        'pass_resume_selected_applications',
        'fail_selected_applications',
    ]

    def fail_selected_applications(self, request, queryset):
        app_len = len(queryset)
        updated_cnt = queryset\
            .filter(status=CampaignApplication.StatusType.new.name)\
            .update(status=CampaignApplication.StatusType.refused_resume.name)

        if updated_cnt > 0:
            self.message_user(
                request,
                "You have succefully refused %d applications" % updated_cnt,
                messages.SUCCESS
            )

        if app_len > updated_cnt:
            self.message_user(
                request,
                "There %d applications that were not new" % (app_len - updated_cnt),
                messages.ERROR
            )

    def pass_resume_selected_applications(self, request, queryset):
        """
        Sep 2020 event - all candidates will do the test at a specific time
        """
        success_app_cnt = 0
        error_app_cnt = 0
        for campaign_app in queryset.filter(status=StatusType.new.name):
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
                    .update(status=StatusType.passed_resume.name)

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


class GroupCampaignAdmin(admin.ModelAdmin):
    list_display = [f.name for f in GroupCampaign._meta.fields]


admin.site.register(GroupCampaign, GroupCampaignAdmin)


class GroupApplicationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in GroupApplication._meta.fields]


admin.site.register(GroupApplication, GroupApplicationAdmin)


class IndividualApplicantAdmin(admin.ModelAdmin):
    list_display = [f.name for f in IndividualApplicant._meta.fields]


admin.site.register(IndividualApplicant, IndividualApplicantAdmin)
