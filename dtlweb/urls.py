# -*- coding: utf-8 -*-
"""dtlweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.shortcuts import redirect

from recruitment_campaign import views


def redirect_to_careers(request):
    return redirect('/careers')


urlpatterns = [
    url(r'^dtlweb/admin/', admin.site.urls),
    url(r'^dtlweb/campaign/', include('recruitment_campaign.urls')),  # Oct 26 2021
    # url(r'^dtlweb/campaign/', redirect_to_careers),  # Oct 26 2021
    url(r'^dtlweb/media/campaign/resumes/(?P<file_name>.+)$', views.download_resume, name='campaign.download_resume'),
    url(r'^dtlweb/', include('main.urls')),
    # url(  # Oct 26 2021
    #     r'^dtlweb/careers/campaign/inviation/(?P<hashstr>[\w:]+)/(?P<action>((accept)|(refuse)))$',
    #     views.accept_invitation_to_attend_campaign,
    #     name='campaign.career.invitation',
    # ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
