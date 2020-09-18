#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from models import ConfigEntry


SIDEBAR_MENU_ITEMS = [
    ('Overview', 'main.career.overview'),
    ('Opening Jobs', 'main.career.jobs'),
    ('Online Application', 'main.career.apply'),
    # ('2020中国招聘', 'chinaevent.career_talk'),
]


def get_sidebar_menu_items(items=SIDEBAR_MENU_ITEMS):
    config_entry = ConfigEntry.objects.filter(name='sidebar_menu_items')
    if len(config_entry) > 0:
        config_entry = config_entry.get()
        items = json.loads(config_entry.extra)

    return items
