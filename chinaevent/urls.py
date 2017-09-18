from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^beijing$', views.beijing_2018, name='chinaevent.beijing2018'),
    url(r'^register$', views.register, name='chinaevent.register'),
]

