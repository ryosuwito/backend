# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from main.models import OnlineApplication, TestRequest

from .models import SITE_CHOICES_MAP
from .forms import OnsiteRegistrationForm


WRITTEN_TEST = [
    {
        'university': '北京大学',
        'location': '待定',
        'time': '2018年10月20日, 09:00 - 12:00',
    },
    {
        'university': '复旦大学',
        'location': '叶耀珍楼会议室202',
        'time': '2018年10月20日, 09:00 - 12:00',
    },
    {
        'university': '上海交通大学',
        'location': '闵行校区数学楼一楼大会议室',
        'time': '2018年10月20日, 09:00 - 12:00',
    },
]

CAREER_TALK = [
    {
        'university': '北京大学宣讲会',
        'location': '新太阳学生中心212室',
        'time': '2018年10月19日, 19:00 - 21:00',
        'mapid': 'loc1',
    },
    {
        'university': '清华大学交流会',
        'location': 'FIT楼1-312',
        'time': '2018年10月17日, 19:00 - 21:00',
        'mapid': 'loc2',
    },
    {
        'university': '复旦大学宣讲会',
        'location': '邯郸校区光华楼主楼1501',
        'time': '2018年10月15日, 19:00 - 21:00',
        'mapid': 'loc3',
    },
    {
        'university': '上海交通大学宣讲会',
        'location': '闵行校区数学楼一楼大会议室',
        'time': '2018年10月16日, 19:00 - 21:00',
        'mapid': 'loc4',
    },
]


def career_talk(request):
    return render(request, "chinaevent/career_talk.html", { 'talks': CAREER_TALK })


def register(request, req_id, hashstr):

    def get_context(test_request):
        context = {
            'form': OnsiteRegistrationForm(instance=test_request.application),
            'career_talks': CAREER_TALK,
            'tests': WRITTEN_TEST,
            'test_req_link': test_request.get_absolute_url(),
            'show_online_schedule_link': True,
        }
        if test_request.application.test_site not in ['', None]:
            context['form'] = None
            context['form_msg'] = 'You already registered for site: %s'\
                % SITE_CHOICES_MAP[test_request.application.test_site]
            context['show_online_schedule_link'] = False

        return context

    test_request = get_object_or_404(TestRequest, pk=req_id, hashstr=hashstr)
    if not test_request.application.is_onsite_recruiment:
        raise Http404()

    template = "chinaevent/register.html"

    if not request.POST:
        return render(request, template, get_context(test_request))
    else:
        # handle post request
        form = OnsiteRegistrationForm(request.POST, instance=test_request.application)
        if form.is_valid():
            model_instance = form.save()
            test_request.application.refresh_from_db()
            return render(request, template, get_context(test_request))
        else:
            return render(request, template, get_context(test_request))
