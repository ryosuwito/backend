# -*- coding: utf-8 -*-
import datetime

from django.contrib import (
    admin,
    messages,
)
from django.urls import reverse_lazy
from main.models import (
    OnlineApplication,
    TestRequest,
    InternCandidate,
    OpenJob,
    ConfigEntry,
)
from main.forms import OpenJobForm
from main.types import (
    JobType,
    JobPosition,
    Workplace,
)
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from recruitment_campaign.models import (
    Campaign,
    CampaignApplication,
)

from . import emails


def get_enum_val(enum_obj, obj_prop_name):
    def get_val(obj):
        obj_prop_value = getattr(obj, obj_prop_name, '')
        enum_value = getattr(enum_obj, obj_prop_value, None)
        return obj_prop_value if enum_value is None else enum_value.value

    get_val.short_description = obj_prop_name
    return get_val


@admin.register(OnlineApplication)
class OnlineApplicationAdmin(admin.ModelAdmin):
    actions = ['invite_selected_apps_to_attend_the_active_campaign']

    def invite_selected_apps_to_attend_the_active_campaign(self, request, queryset):
        campaigns = Campaign.objects.filter(active=True)
        if len(campaigns) != 1:
            self.message_user(
                request,
                "There is no or more than one campaign being active at the moment",
                messages.ERROR,
            )
            return
        else:
            campaign = campaigns.get()
            cnt = 0
            for app in queryset.filter(~Q(status=OnlineApplication.APP_STATUS_CAMPAIGN)):
                try:
                    req = TestRequest.createTestRequestForApplication(app)
                    CampaignApplication.objects.create(
                        campaign=campaign,
                        application=app,
                        status=CampaignApplication.StatusType.invited.name
                    )
                    app.status = OnlineApplication.APP_STATUS_CAMPAIGN
                    app.save(update_fields=('status',))
                    # send invitation email
                    relative_accept_url = str(
                        reverse_lazy(
                            'campaign.career.invitation',
                            kwargs={'hashstr': req.hashstr, 'action': 'accept'},
                        )
                    )
                    relative_refuse_url = str(
                        reverse_lazy(
                            'campaign.career.invitation',
                            kwargs={'hashstr': req.hashstr, 'action': 'refuse'},
                        )
                    )
                    context = {
                        "application": app,
                        "test_request": req,
                        # TODO site host should be stored in settings for in the database request.build_absolute_uri
                        # could go wrong when it is a service behind proxy server.
                        "accept_url": request.build_absolute_uri(relative_accept_url),
                        "refuse_url": request.build_absolute_uri(relative_refuse_url),
                        "campaign": campaign,
                    }
                    emails.send_invitation_to_attend_recuitment_campaign(context)
                    cnt += 1
                except Exception as err:
                    print(err)
                    self.message_user(request, "Failed to invite %s" % app.email, messages.ERROR)

            if cnt > 0:
                self.message_user(
                    request,
                    "Invited successfully %d candidates to attend the campaign %s" % (cnt, campaign.name),
                    messages.SUCCESS,
                )

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

        if obj.is_intern:
            # 3 months for FULL-TIME INTERNSHIP
            # 4 months for PART-TIME INTERNSHIP
            days = 120 if obj.typ == JobType.PARTTIME_INTERNSHIP.name else 90
            end_time = start_time + datetime.timedelta(days=days)
        else:
            end_time = None

        start_time = start_time.strftime('%Y.%m.%d')
        end_time = 'oo' if end_time is None else end_time.strftime('%Y.%m.%d')

        return '{}-{}'.format(start_time, end_time)

    get_scheduled_test.short_description = "Scheduled Test"
    list_display = ('name', 'university', 'school', 'major', 'email',
                    get_enum_val(JobPosition, 'position'), get_enum_val(JobType, 'typ'),
                    'need_work_pass',
                    get_enum_val(Workplace, 'workplace'), start_and_end_time, 'status',
                    get_scheduled_test, 'info_src', 'from_china_event', 'test_site', 'created_at')

    list_editable = ('status',)
    list_filter = ('typ', 'workplace', 'position', 'status', 'is_onsite_recruiment', 'test_site',)
    search_fields = ('name', 'university', 'school', 'major', 'email')


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
    list_display = ('id', 'typ', 'workplace', 'position', 'active', 'test_id')
    list_display_links = ('id',)
    list_editable = ('active', 'test_id')
    list_filter = ('position', 'typ', 'workplace', 'active', 'test_id')
    form = OpenJobForm


@admin.register(ConfigEntry)
class ConfigEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'extra')
    list_display_links = ('name',)
    list_editable = ('value', 'extra')
