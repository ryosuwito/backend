import traceback
import logging
import jwt

from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings

from django.shortcuts import (
    render,
    get_object_or_404,
    Http404,
)
from django.views.decorators.http import require_http_methods

# Create your views here.
from main.emails import (
    send_online_application_confirm,
    send_online_application_summary,
)
from main import templatedata
from main.models import (
    OnlineApplication,
    TestRequest,
)

from .models import (
    Campaign,
    CampaignApplication,
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
    context = {
        'sidebar_menu_items': templatedata.get_sidebar_menu_items(),
    }

    if len(campaign) == 0:
        if request.method == 'GET':
            context['message'] = {'info': 'There is no campaign this time.'}
            return render(request, "recruitment_campaign/career_apply.html", context)
        else:
            context['message'] = {'error': 'Forbidden action.'}
            return render(request, "recruitment_campaign/career_apply.html", status=403)
    else:
        campaign = campaign.get()
        context['campaign'] = campaign
        if request.method == 'GET':
            context.update({'form': CampaignApplicationForm()})
            return render(request, "recruitment_campaign/career_apply.html", context)
        else:
            # Handle POST request
            form = CampaignApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                model_instance = form.save(commit=False)
                model_instance.status = OnlineApplication.APP_STATUS_CAMPAIGN
                model_instance.save()
                CampaignApplication.objects.create(
                    campaign_id=campaign.id, application_id=model_instance.id
                )
                try:
                    handle_application_form(model_instance)
                    context.update({'form': None})
                    return render(request, "main/career_apply_confirm.html", context)
                except:
                    logger.error(traceback.format_exc())
                    model_instance.delete()
                    context.update({'form': form})
                    return render(request, "recruitment_campaign/career_apply.html", context)
            else:
                context.update({'form': form})
                return render(request, "recruitment_campaign/career_apply.html", context)


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
