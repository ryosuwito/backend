# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^careers/apply$', views.apply, name='main.career.apply'),
    url(r'^careers/success_application$', views.success_application, name='main.career.success_application'),
    url(r'^careers/$', views.apply, name='main.career'),
    url(r'^careers/test/(?P<req_id>[0-9]+)/(?P<hashstr>[\w:]+)$', views.career_test, name='main.career.test'),
    url(r'^media/resumes/(?P<file_name>.+)$', views.download_resume,
        name='main.download_resume'),
    url(r'^api/career_data$', views.career_data, name='main.career.career_data'),
]
