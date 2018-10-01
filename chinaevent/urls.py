# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.career_talk, name='chinaevent.career_talk'),
    url(r'^career_talk$', views.career_talk, name='chinaevent.career_talk'),
    url(r'^register/(?P<req_id>[0-9]+)/(?P<hashstr>[\w:]+)$', views.register, name='chinaevent.register'),
]

