# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^apply$', views.career_apply, name='recruitmentcampaign.apply'),
    url(r'^careers/success_application$', views.success_application, name='recruitmentcampaign.success_application'),
    url(r'^careers/$', views.career_apply, name='recruitmentcampaign.career'),
    url(r'', views.career_apply, name='recruitmentcampaign.home'),
]
