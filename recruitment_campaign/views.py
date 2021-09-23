# -*- coding: utf-8 -*-
import traceback
import logging
import jwt
import json
import os
import mimetypes
import uuid

from wsgiref.util import FileWrapper

from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.dateparse import parse_datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from django.forms.models import model_to_dict

from django.shortcuts import (
    render,
    get_object_or_404,
    Http404,
    redirect,
    HttpResponse,
)
from django.urls import reverse
from django.views.decorators.http import require_http_methods

# Create your views here.

from main.models import (
    OnlineApplication,
    TestRequest,
)

from .models import (
    CampaignOnlineApplication,
    CampaignApplication,
    Campaign,
    EventLog,
)
from .emails import (
    send_online_application_confirm,
    send_online_application_summary,
    send_token_email,
)
from .forms import CampaignApplicationForm
from .types import ApplicationStatus2021

from main import cron
from main import emails as main_emails


logger = logging.getLogger(__name__)


def handle_application_form(application):
    # send application form summary to company email
    send_online_application_summary(application)
    # send confirmation email to candidate
    send_online_application_confirm(application)


@require_http_methods(["GET", "POST"])
def career_apply(request):
    campaign = Campaign.objects.filter(active=True)
    context = {}

    if len(campaign) == 0:
        raise Http404
    else:
        campaign = json.loads(campaign[0].meta_data)
        context['campaign'] = campaign
        if request.method == 'GET':
            context.update({'form': CampaignApplicationForm(campaign)})
            return render(request, "recruitment_campaign/career_apply.html", context)
        else:
            # Handle POST request
            form = CampaignApplicationForm(campaign, request.POST, request.FILES)
            if form.is_valid():
                model_instance = form.save()
                try:
                    handle_application_form(model_instance)
                    context.update({'form': None})
                    return redirect(reverse('recruitmentcampaign.success_application'))
                except:
                    logger.error(traceback.format_exc())
                    model_instance.delete()
                    context.update({'form': form})
                    return render(request, "recruitment_campaign/career_apply.html", context)
            else:
                context.update({'form': form})
                return render(request, "recruitment_campaign/career_apply.html", context)


@login_required
def download_resume(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'campaign/resumes', file_name)
    if not os.path.isfile(file_path):
        raise Http404()

    file_wrapper = FileWrapper(file(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(file_path))
    return response


@require_http_methods(["GET"])
def success_application(request):
    return render(request, "recruitment_campaign/application_success.html")


@require_http_methods(["GET"])
def accept_invitation_to_attend_campaign(request, hashstr, action):
    test_request = get_object_or_404(TestRequest, hashstr=hashstr)
    campaign_application = get_object_or_404(CampaignApplication, application=test_request.application)
    campaign = campaign_application.campaign
    context = {"campaign": campaign}

    if test_request.token_status == cron.TOKEN_READY or test_request.token_status == cron.TOKEN_SENT:
        # Already accept the the invitation
        context['token_ready'] = True
        return render(request, "recruitment_campaign/accept_invitation.html", context)

    if action == 'accept':
        # Create a token
        payload = {
            'username': get_random_string(15),
            'password': get_random_string(15),
            'timestamp': cron.timestamp(timezone.now()),
            'start_time_timestamp': cron.timestamp(campaign.starttime),
            'fullname': test_request.application.name,
            'test_id': campaign.test_id,
            'email': test_request.application.email,
        }
        token = jwt.encode(payload, settings.SHARE_KEY, 'HS256')
        test_request.refresh_from_db()
        test_request.token = token
        test_request.token_status = cron.TOKEN_READY
        test_request.status = TestRequest.STATUS_SET
        test_request.datetime = campaign.starttime
        test_request.save(update_fields=('token', 'token_status', 'status', 'datetime'))
        CampaignApplication.objects\
            .filter(id=campaign_application.id)\
            .update(status=CampaignApplication.StatusType.accept_invitation.name)

        context['test_request'] = test_request

        return render(request, "recruitment_campaign/accept_invitation.html", context)
    elif action == 'refuse':
        application = test_request.application
        application.status = OnlineApplication.APP_STATUS_PASS_RESUME
        application.save(update_fields=('status',))
        CampaignApplication.objects\
            .filter(id=campaign_application.id)\
            .update(status=CampaignApplication.StatusType.refuse_invitation.name)

        return render(request, "recruitment_campaign/refuse_invitation.html", context)
    else:
        raise Http404()


@require_http_methods(["GET"])
def accept_invite_2021(request, token):
    # check if the application status is invite_sent, if it's not display a message
    event_log = get_object_or_404(EventLog, name=token)
    data = json.loads(event_log.data)
    campaign = get_object_or_404(Campaign, pk=data.get('campaign'))
    application = get_object_or_404(CampaignOnlineApplication, pk=data.get('application'))
    token_event_log = get_object_or_404(EventLog, pk=data.get('token_event_id'))
    token_event_data = json.loads(token_event_log.data)
    if application.status == ApplicationStatus2021.INVITE_SENT.name:
        # send email containing credentials
        email_context = {
            'username': token_event_data['payload']['username'],
            'password': token_event_data['payload']['password'],
            'host': settings.ONLINE_TEST_HOST,
            'application': application,
            'starttime': parse_datetime(token_event_data['test']['time']).strftime("%H:%M:%S"),
            'duration': token_event_data['test']['duration'],
        }
        send_token_email(email_context)
        # update application
        application.refresh_from_db()
        application.status = ApplicationStatus2021.INVITE_ACCEPTED.name
        application.save(update_fields=('status',))
        return render(request, 'recruitment_campaign/invite_accept_2021.html', {'title': campaign.name})
    elif application.status == ApplicationStatus2021.INVITE_ACCEPTED.name:
        # has  already accepted
        return render(
            request,
            'recruitment_campaign/invite_accept_2021.html',
            {'have_already_accepted': True, 'title': campaign.name}
        )

    raise Http404()


@require_http_methods(["GET"])
def refuse_invite_2021(request, token):
    # check if the application status is invite_sent, if it's not display a message
    event_log = get_object_or_404(EventLog, name=token)
    data = json.loads(event_log.data)
    campaign = get_object_or_404(Campaign, pk=data.get('campaign'))
    application = get_object_or_404(CampaignOnlineApplication, pk=data.get('application'))
    campaign_data = json.loads(campaign.meta_data)
    # update application

    if application.status == ApplicationStatus2021.INVITE_SENT.name:
        online_app_data = model_to_dict(
            application,
            fields=['position', 'typ', 'workplace', 'name', 'university', 'school', 'major', 'email', 'resume'])

        for field in ['position', 'typ', 'workplace']:
            current_value = online_app_data[field]
            online_app_data[field] = campaign_data['data_mapping'][current_value]

        online_app_data['status'] = OnlineApplication.APP_STATUS_CAMPAIGN
        unique_str = uuid.uuid4()
        OnlineApplication.objects \
            .filter(email=online_app_data['email']) \
            .update(email="{}__{}".format(str(unique_str), online_app_data['email']))
        online_app = OnlineApplication(**online_app_data)
        online_app.save()
        test_request = TestRequest.createTestRequestForApplication(online_app)
        main_emails.send_test_request(test_request)
        application.status = ApplicationStatus2021.INVITE_REFUSED.name
        application.save(update_fields=('status',))
        return render(
            request,
            'recruitment_campaign/invite_refuse_2021.html',
            {'title': campaign.name, 'test_request': test_request}
        )
    elif application.status == ApplicationStatus2021.INVITE_REFUSED.name:
        # have already refused the joint test
        return render(
            request,
            'recruitment_campaign/invite_refuse_2021.html',
            {'have_already_refused': True, 'title': campaign.name}
        )

    raise Http404
