from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='main.index'),
    url(r'^careers/overview$', views.career_overview, name='main.career.overview'),
    url(r'^careers/jobs$', views.career_jobs, name='main.career.jobs'),
    url(r'^careers/apply$', views.career_apply, name='main.career.apply'),
    url(r'^careers/chinaevent$', views.career_chinaevent, name='main.career.chinaevent'),
    url(r'^careers/test/(?P<req_id>[0-9]+)/(?P<hashstr>[\w:]+)$', views.career_test, name='main.career.test'),
    url(
        r'^culture/overview$',
        views.culture_overview,
        name='main.culture.overview'
    ),
    url(
        r'^culture/atwork$',
        views.culture_atwork,
        name='main.culture.atwork'
    ),
    url(
        r'^culture/offwork$',
        views.culture_offwork,
        name='main.culture.offwork'
    ),
    url(r'^contact$', views.contact, name='main.contact'),
    url(r'^what$', views.what_we_do, name='main.what'),
]
