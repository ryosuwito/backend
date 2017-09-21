# -*- coding: utf-8 -*-
from django.shortcuts import render

from .forms import RegistrationForm


WRITTEN_TEST_2018 = {
    '北京': [
        {
            'university': '北京大学',
            'location': '理科一号楼1114',
            'time': '2017年10月14日，09:00-12:00',
            'mapid': 'loc1'
        },
    ],
    '上海': [
        {
            'university': '复旦大学',
            'location': '张江校区软件楼102第二会议室',
            'time': '2017年10月14日, 09:00-12:00',
            'mapid': 'loc2'
        },
        {
            'university': '上海交通大学',
            'location': '闵行校区数学楼一楼大会议室',
            'time': '2017年10月14日, 09:00-12:00',
            'mapid': 'loc3'
        },
    ]
}


CAREER_TALK_2018 = {
    '北京': [
        {
            'university': '北京大学',
            'location': '新太阳学生中心212',
            'time': '2017年10月09日, 14:00-16:00',
            'mapid': 'loc1'
        },
        {
            'university': '清华大学',
            'location': '伟伦楼501',
            'time': '2017年10月12日, 19:00-21:00',
            'mapid': 'loc2'
        },
    ],
    '上海': [
        {
            'university': '复旦大学',
            'location': '张江校区第二教学楼2301教室',
            'time': '2017年10月10日, 19:00-21:00',
            'mapid': 'loc3'
        },
        {
            'university': '上海交通大学',
            'location': '闵行校区数学楼一楼大会议室',
            'time': '2017年10月11日, 19:00-21:00',
            'mapid': 'loc4'
        },
    ]
}


def career_talk(request):
    return render(request, "chinaevent/career_talk.html", { 'tests': CAREER_TALK_2018 })


def register(request):
    template = "chinaevent/register.html"
    confirm_template = "chinaevent/register_confirm.html"
    if not request.POST:
        return render(request, template, {'form': RegistrationForm(), 'tests': WRITTEN_TEST_2018})
    else:
        # handle post request
        form = RegistrationForm(request.POST)
        if form.is_valid():
            model_instance = form.save()
            return render(request, confirm_template, {
                'form': None,
                'tests': WRITTEN_TEST_2018
            })
        else:
            return render(request, template, {'form': form, 'tests': WRITTEN_TEST_2018})
