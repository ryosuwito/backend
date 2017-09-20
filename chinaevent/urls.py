from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^career_talk$', views.career_talk, name='chinaevent.career_talk'),
    url(r'^register$', views.register, name='chinaevent.register'),
]

