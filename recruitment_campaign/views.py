import traceback
import logging
import jwt
import json
import os
import mimetypes

from wsgiref.util import FileWrapper

from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str

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
    Campaign,
    CampaignApplication,
)
from .emails import (
    send_online_application_confirm,
    send_online_application_summary,
)
from .forms import CampaignApplicationForm

from main import cron


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
