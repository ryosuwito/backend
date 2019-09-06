# -*- coding: utf-8 -*-
import os
import logging
import mimetypes
import traceback
from django.conf import settings
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str

from wsgiref.util import FileWrapper

from main.models import TestRequest, OnlineApplication
from main.forms import OnlineApplicationForm, TestRequestForm, InternApplicationForm
from main.emails import send_online_application_confirm, send_online_application_summary

from main import templatedata


logger = logging.getLogger(__name__)

SIDEBAR_MENU_ITEMS = templatedata.SIDEBAR_MENU_ITEMS


def index(request):
    return render(request, "main/main_page.html")


def career_apply(request):

    def handle_application_form(application):
        # send application form summary to company email
        send_online_application_summary(application)
        # send confirmation email to candidate
        send_online_application_confirm(application)

    context = {
        'sidebar_menu_items': SIDEBAR_MENU_ITEMS,
    }

    if not request.POST:
        context.update({'form': OnlineApplicationForm()})
        return render(request, "main/career_apply.html", context)
    else:
        # Handle POST request
        form = OnlineApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            try:
                handle_application_form(model_instance)
                context.update({'form': None})
                return render(request, "main/career_apply_confirm.html", context)
            except:
                logger.error(traceback.format_exc())
                model_instance.delete()
                context.update({'form': form})
                return render(request, "main/career_apply.html", context)
        else:
            context.update({'form': form})
            return render(request, "main/career_apply.html", context)


def career_apply_intern(request, template="main/career_apply_intern.html"):

    def handle_intern_application_form(application):
        # auto update status of the application to PASS_RESUME
        application.status = OnlineApplication.APP_STATUS_PASS_RESUME
        application.save()

    if not request.POST:
        return render(request, template, {
            'form': InternApplicationForm() })
    else:
        # Handle POST request
        form = InternApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            try:
                handle_intern_application_form(model_instance)
                return render(request, "main/career_apply_confirm.html",
                              {'form': None})
            except:
                logger.error(traceback.format_exc())
                model_instance.delete()
                return render(request, template, {'form': form})
        else:
            return render(request, template, {'form': form})


def career_test(request, req_id, hashstr):
    test_request = get_object_or_404(TestRequest, pk=req_id)
    if test_request.status == TestRequest.STATUS_SENT:
        return HttpResponse(
            "The test request is expired. Email was sent to you. If you did not receive \
            the email, please send us email via careers@dytechlab.com.")
    if hashstr != test_request.hashstr:
        raise Http404("This link does not exist.")

    template = "main/career_testreq.html"
    form = TestRequestForm(instance=test_request)

    if not request.POST:
        return render(request, template, {
            'form': form,
            'is_set': test_request.datetime\
                      if test_request.status == TestRequest.STATUS_SET else None,
            'allow_update': test_request.allow_update()
        })
    else:
        # Handle POST Request
        form = TestRequestForm(request.POST, instance=test_request)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.status = TestRequest.STATUS_SET
            model_instance.save()
            return render(request, template, {
                'form': TestRequestForm(instance=test_request),
                'is_set': model_instance.datetime,
                'allow_update': model_instance.allow_update()
            })
        else:
            return render(request, template, {
                'form': form,
                'is_set': test_request.datetime\
                          if test_request.status == TestRequest.STATUS_SET else None,
                'allow_update': test_request.allow_update()
            })


def career_jobs(request):
    from main.data import positions
    context = {
        'sidebar_menu_items': SIDEBAR_MENU_ITEMS,
        'positions': positions,
    }
    return render(request, "main/career_job_opening.html", context)


def career_overview(request):
    # flake8: noqa
    context = {
        'sidebar_menu_items': SIDEBAR_MENU_ITEMS,
        'why_dtl': [
            {
                "desc": """Learn from the Best""",
                "content": """Our employees are top-notch talents in their fields. Though they come with diverse background, they share a common drive to succeed. As DTL's new employee, you could learn from our experienced mentors. We strive to maintain a friendly, collegiate working environment to promote self-improvement and career development."""},
            {
                "desc": """Receive thorough Training""",
                "content": """A job offer at DTL is the start of our investment in you. Based on your background, we will develop specific programs and provide resources ( books, papers, tutorials etc. ) to help you build and enhance your skills in finance, mathematics, statistics and programming."""},
            {
                "desc": """Share Our Success""",
                "content": """We are a specialized investment team with excellent track record. By joining us, you will grow together with the company. Your remuneration will be based on your performance and the company's performance as a whole. We offer highly competitive compensation packages."""},
            {
                "desc": """Make A Difference""",
                "content": """You can really make a difference even during entry-level as you will be tasked with challenging yet interesting assignments. We strive to help you in every way to facilitate innovation and brainstorm fresh ideas which are the key to our success."""}
        ]
    }
    return render(request, "main/career_overview.html", context)


def culture_overview(request):
    cultures = [
        {
            'desc': 'Value Our Greatest Asset',
            'content': 'Employees are our most valuable asset and we try our best to provide opportunities for everyone to achieve and realize their potential. All employees, regardless of their positions or experience, are well respected and grow together with the company.',
        },
        {
            'desc': 'Never Stop Thinking',
            'content': 'To stand out in fiercely competitive markets we always keep a sharp mind, generate fresh ideas, and stand ready to solve complex problems. All innovative ideas are fully recognized and highly rewarded.'
        },
        {
            'desc': 'Focus on Cutting-edge Tech',
            'content': 'At DTL all the works are technology-oriented. We consider ourselves more as engineers or scientists than financial practitioners. Our success depends on the continuous focus on adopting the latest technology in computer science, math, statistics, and finance.'
        },
        {
            'desc': 'Work Hard, Play Hard',
            'content': 'Working is important but life is more than just work. We regularly organize team events like outings, dining parties and sports events. To each other, we are both hardworking colleagues at work and close friends in life.'
        },
    ]

    return render(request, "main/culture_overview.html", { 'cultures': cultures })


def culture_atwork(request):
    atworks = [
        {
            'desc': 'We maintain a flat management structure. Juniors are encouraged to discuss with or challenge the seniors for ideas. With an open culture, any suggestions could be brought up to senior management and major decisions will be made with full consideration of all employees in the company.',
            'img': 'main/img/pool/tangfengyang.003.jpeg'
        },
        {
            'desc': 'Though a significant amount of work is done individually, our work nature demands a lot of cooperation among researchers, data scientists, developers, traders and portfolio managers. We work together to achieve our shared goals.',
            'img': 'main/img/pool/tangfengyang.002.jpeg'
        },
        {
            'desc': 'To foster a culture of innovation we have weekly research presentations where all researchers get together to share their findings and ideas. There are also regular meetings to discuss how to improve our systems and operations.',
            'img': 'main/img/pool/tangfengyang.004.jpeg'
        },
        {
            'desc': 'We strive to maintain a casual, flexible and comfortable working environment to maximize productivity. We do not have any specific dress code and plenty of refreshments like fruits and snacks is provided.',
            'img': 'main/img/pool/tangfengyang.001.jpeg'
        },
    ]
    return render(request, "main/culture_atwork.html", { 'atworks': atworks})


def culture_offwork(request):
    offworks = [
        {
            'desc': 'We organize regular dining parties on festive occasions or to celebrate the joining of new colleagues.',
            'img': 'main/img/offoffice/p1.jpg'
        },
        {
            'desc': 'There are plenty of sports facilities nearby including tennis/ping pong/basketball courts, swimming pool and gym etc. Our employees play all sorts of sports so you could always find someone to play with.',
            'img': 'main/img/offoffice/p2.jpg'
        },
        {
            'desc': 'There are many ways for entertainment like KTV, billiard, chess or Texas Hold\'em. If you would like to explore the wild, hiking and diving are also accessible. DTL encourages employees to pursue their hobbies off work.',
            'img': 'main/img/offoffice/p3.jpg'
        },
        {
            'desc': 'Our employees go jogging on a regular basis. DTL also sponsors interested employees to participate in the annual Standard Chartered Marathon.',
            'img': 'main/img/offoffice/p4.jpg'
        },
    ]

    return render(request, "main/culture_offwork.html", {'offworks': offworks})


def what_we_do(request):
    return render(request, "main/what_we_do.html")


def contact(request):
    return render(request, "main/contact.html")


@login_required
def download_resume(request, file_name):
    import glob
    file_path = os.path.join(settings.MEDIA_ROOT, 'resumes', file_name)
    if not os.path.isfile(file_path):
        # get the first file start with file_name
        for fn in glob.glob('{}*'.format(file_path)):
            file_path = fn
            break
    if not os.path.isfile(file_path):
        raise Http404()

    file_wrapper = FileWrapper(file(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(file_path))
    return response
