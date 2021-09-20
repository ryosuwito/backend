import json

from .models import OpenJob
from .models import ConfigEntry
from .types import (
    Workplace,
    JobPosition,
    JobType,
    ConfigKey,
)


def get_given_time(req):
    given_time = None
    try:
        app = req.application
        open_job = OpenJob.objects.get(position=app.position, typ=app.typ, workplace__contains=app.workplace)
        given_time = open_job.test_duration
    except Exception:
        pass

    return given_time


def get_workplace_dict():
    try:
        config_entry = ConfigEntry.objects.get(name=ConfigKey.JOB_WORKPLACE.value)
        ret = json.loads(config_entry.extra)
    except ConfigEntry.DoesNotExist:
        ret = {wp.name:wp.value for wp in Workplace}

    return ret


def get_position_dict():
    try:
        config_entry = ConfigEntry.objects.get(name=ConfigKey.JOB_POSITION.value)
        ret = json.loads(config_entry.extra)
    except ConfigEntry.DoesNotExist:
        ret = {jp.name:jp.value for jp in JobPosition}

    return ret


def get_jobtype_dict():
    try:
        config_entry = ConfigEntry.objects.get(name=ConfigKey.JOB_TYPE.value)
        ret = json.loads(config_entry.extra)
    except ConfigEntry.DoesNotExist:
        ret = {jtype.name:jtype.value for jtype in JobType}

    return ret
