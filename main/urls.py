from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^career$', views.career, name='career'),
    url(r'^culture$', views.culture, name='culture'),
]
