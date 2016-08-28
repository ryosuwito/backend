from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='main.index'),
    url(r'^career$', views.career, name='main.career'),
    url(r'^request$', views.online_test_request, name='main.request'),
    url(r'^culture$', views.culture, name='main.culture'),
]
