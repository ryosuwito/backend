# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^apply$', views.career_apply, name='recruitmentcampaign.apply'),
    url(r'^careers/success_application$', views.success_application, name='recruitmentcampaign.success_application'),
    url(r'^careers/success_registration$', views.success_registration, name='recruitmentcampaign.success_registration'),
    url(r'^careers/$', views.career_apply, name='recruitmentcampaign.career'),
    url(r'^jointtest_invitation/accept/(?P<token>[\w-]+)',
        views.accept_invite_2021,
        name='recruitmentcampaign.invite2021.accept'),

    url(r'^jointtest_invitation/refuse/(?P<token>[\w-]+)',
        views.refuse_invite_2021,
        name='recruitmentcampaign.invite2021.refuse'),

    url(r'group/$', views.group_apply, name='recruitmentcampaign.group'),
    url(r'', views.career_apply, name='recruitmentcampaign.home'),
]
