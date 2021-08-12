# -*- coding: utf-8 -*-
import os
import logging
import mimetypes
import copy
import json
from django.conf import settings
from django.shortcuts import (
    render,
    get_object_or_404,
    HttpResponse,
    redirect,
)
from django.urls import reverse
from django.http import (
    Http404,
    JsonResponse,
)
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from django.forms.models import model_to_dict

from wsgiref.util import FileWrapper

from main.models import (
    TestRequest,
    OpenJob,
    ConfigEntry,
)
from main.forms import (
    OnlineApplicationForm,
    TestRequestForm,
)
from main.emails import (
    send_online_application_confirm,
    send_online_application_summary,
)
from main import helper

from types import ConfigKey

from django.views.decorators.http import require_http_methods


logger = logging.getLogger(__name__)


def index(request):
    return render(request, "main/main_page.html")


@require_http_methods(["GET", "POST"])
def apply(request):

    def handle_application_form(application):
        # send application form summary to company email
        send_online_application_summary(application)
        # send confirmation email to candidate
        send_online_application_confirm(application)

    context = {'form': None}

    if request.method == 'GET':
        ALLOWED_FIELDS = {'position', 'typ', 'workplace'}
        initial_data = dict(list(filter(lambda x: x[0] in ALLOWED_FIELDS, copy.deepcopy(request.GET).items())))
        context.update({'form': OnlineApplicationForm(initial=initial_data)})
        return render(request, "main/application_form.html", context)
    else:
        # Handle POST request
        form = OnlineApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            model_instance = form.save()
            handle_application_form(model_instance)
            return redirect(reverse('main.career.success_application'))
        else:
            context.update({'form': form})
            return render(request, "main/application_form.html", context)


@require_http_methods(["GET"])
def success_application(request):
    return render(request, "main/application_success.html")


@require_http_methods(["GET", "POST"])
def career_test(request, req_id, hashstr):
    test_request = get_object_or_404(TestRequest, pk=req_id)
    if test_request.status == TestRequest.STATUS_SENT:
        return HttpResponse(
            "The test request is expired. Email was sent to you. If you did not receive \
            the email, please send us email via careers@dytechlab.com.")

    if hashstr != test_request.hashstr:
        raise Http404("This link does not exist.")

    template = "main/test_schedule.html"
    form = TestRequestForm(instance=test_request)

    context = {
        'form': form,
        'is_set': test_request.datetime if test_request.status == TestRequest.STATUS_SET else None,
        'allow_update': test_request.allow_update(),
        'given_time': helper.get_given_time(test_request),
    }

    if request.method == "GET":
        return render(request, template, context)
    else:
        # Handle POST Request
        form = TestRequestForm(request.POST, instance=test_request)
        context.update({'form': form})
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.status = TestRequest.STATUS_SET
            model_instance.save()
            return redirect(
                reverse('main.career.test', kwargs={"req_id": test_request.id, "hashstr": test_request.hashstr}))
        else:
            return render(request, template, context)


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


@require_http_methods(["GET"])
def career_data(request):
    open_jobs = OpenJob.objects.filter(active=True)
    open_jobs = list(map(lambda x: model_to_dict(x), open_jobs))
    positions = json.loads(ConfigEntry.objects.get(name=ConfigKey.JOB_POSITION.value).extra)
    types = json.loads(ConfigEntry.objects.get(name=ConfigKey.JOB_TYPE.value).extra)
    workplaces = json.loads(ConfigEntry.objects.get(name=ConfigKey.JOB_WORKPLACE.value).extra)
    config_entry = ConfigEntry.objects.filter(name=ConfigKey.CAREER_META_DATA.value)
    meta_data = None
    if len(config_entry) > 0:
        config_entry = config_entry[0]
        meta_data = json.loads(config_entry.extra)

    ret = {
        "positions": positions,
        "types": types,
        "workplaces": workplaces,
        "open_jobs": open_jobs,
        "meta_data": meta_data,
    }
    return JsonResponse(ret)
