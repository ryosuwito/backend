# -*- coding: utf-8 -*-
from django.contrib import admin
from chinaevent.models import Candidate


# Register your models here.
@admin.register(Candidate)
class ChinaEventCandidate(admin.ModelAdmin):
    list_display = ('site', 'email', 'name', 'university', 'school', 'major', 'info_src')
    list_filter = ('site',)
