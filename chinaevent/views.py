# -*- coding: utf-8 -*-
import json
import datetime
import logging
import traceback
import copy

from django.http import Http404
from django.shortcuts import render, get_object_or_404

from main.models import TestRequest

from .models import (SITE_CHOICES_MAP, EventContent)
from .forms import (OnsiteRegistrationForm, RegistrationForm)

from main.emails import send_online_application_confirm, send_online_application_summary
from main.types import (
    JobType,
    Workplace,
)

from main import templatedata


logger = logging.getLogger(__name__)


SIDEBAR_MENU_ITEMS = templatedata.SIDEBAR_MENU_ITEMS


def filter_method_decorator(methods=['get', 'post']):
    methods = map(lambda x: x.lower(), methods)

    def wrapper(func):
        def wrapped_func(request, *args, **kwargs):
            if request.method.lower() not in methods:
                raise Http404()
            else:
                return func(request, *args, **kwargs)

        return wrapped_func

    return wrapper


def current_year():
    today = datetime.date.today()
    year = today.year
    return year if today.month < 9 else year + 1


@filter_method_decorator(methods=['get', 'post'])
def career_talk(request, *args, **kwargs):
    year = current_year()
    event_content = EventContent.objects.get(year=year)
    event_content_dict = json.loads(event_content.payload)
    context = {
        'talks': event_content_dict['careerTalks'],
        'tests': event_content_dict['writtenTests'],
        'year': year,
        'sidebar_menu_items': SIDEBAR_MENU_ITEMS,
    }
    if request.method.lower() == 'get':
        context.update({'form': RegistrationForm()})
        return render(request, "chinaevent/career_talk.html", context)
    elif request.method.lower() == 'post':
        def handle_application_form(application):
            # send application form summary to company email
            send_online_application_summary(application)
            # send confirmation email to candidate
            send_online_application_confirm(application)

        # Handle POST request
        data = copy.deepcopy(request.POST)
        form = RegistrationForm(data, request.FILES)
        if form.is_valid():
            model_instance = form.save(commit=False)
            # Update from china event
            model_instance.is_onsite_recruiment = True
            # Workplace is Singapore by default
            model_instance.workplace = Workplace.SINGAPORE.name
            model_instance.save()
            try:
                handle_application_form(model_instance)
                context.update({'form': RegistrationForm(), 'success_apply': True})
                return render(request, "chinaevent/career_talk.html", context)
            except:
                logger.error(traceback.format_exc())
                model_instance.delete()
                context.update({'form': form})
                return render(request, "chinaevent/career_talk.html", context)
        else:
            context.update({'form': form})
            return render(request, "chinaevent/career_talk.html", context)


@filter_method_decorator(methods=['get', 'post'])
def register(request, req_id, hashstr):

    def get_context(test_request):
        year = current_year()
        event_content = EventContent.objects.get(year=year)
        event_content_dict = json.loads(event_content.payload)
        context = {
            'form': OnsiteRegistrationForm(instance=test_request.application),
            'career_talks': event_content_dict['careerTalks'],
            'tests': event_content_dict['writtenTests'],
            'test_req_link': test_request.get_absolute_url(),
            'year': year,
        }
        if test_request.application.test_site not in ['', None]:
            context['form'] = None
            context['form_msg'] = "You've opted the region %s to do onsite test successfully!"\
                % SITE_CHOICES_MAP[test_request.application.test_site]

        return context

    test_request = get_object_or_404(TestRequest, pk=req_id, hashstr=hashstr)
    if not test_request.application.from_china_event:
        raise Http404()

    template = "chinaevent/register.html"

    if not request.POST:
        return render(request, template, get_context(test_request))
    else:
        # handle post request
        form = OnsiteRegistrationForm(request.POST, instance=test_request.application)
        if form.is_valid():
            form.save()
            test_request.application.refresh_from_db()
            return render(request, template, get_context(test_request))
        else:
            return render(request, template, get_context(test_request))
