# -*- coding: utf-8 -*-
from django.contrib import admin
from chinaevent.models import (Candidate, EventContent)


# Register your models here.
@admin.register(Candidate)
class ChinaEventCandidate(admin.ModelAdmin):
    list_display = ('site', 'email', 'name', 'university', 'school', 'major', 'info_src')
    list_filter = ('site',)


@admin.register(EventContent)
class EventContent(admin.ModelAdmin):
    list_display = ('year', 'payload', 'created_at', 'updated_at')
