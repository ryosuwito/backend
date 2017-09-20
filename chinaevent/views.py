# -*- coding: utf-8 -*-
from django.shortcuts import render

from .forms import RegistrationForm


WRITTEN_TEST_2018 = {
    'Beijing': [
        {
            'university': 'Perking 大学 (PKU)',
            'location': 'Center 212',
            'time': '2017 Oct 15th, 2:30 pm',
            'mapid': 'loc1'
        },
    ],
    'Shanghai': [
        {
            'university': 'Fudan University (FDU)',
            'location': 'Center 212',
            'time': '2017 Oct 15th, 2:30 pm',
            'mapid': 'loc2'
        },
        {
            'university': 'Shanghai Jiaotong University (SJTU)',
            'location': 'Center 212',
            'time': '2017 Oct 15th, 2:30 pm',
            'mapid': 'loc3'
        },
    ]
}


CAREER_TALK_2018 = {
    'Beijing': [
        {
            'university': 'Perking (PKU)',
            'location': 'Center 212',
            'time': '2017 Oct 15th, 2:30 pm',
            'mapid': 'loc1'
        },
        {
            'university': 'Another Beijing University (PKU)',
            'location': 'Center 212',
            'time': '2017 Oct 15th, 2:30 pm',
            'mapid': 'loc2'
        },
    ],
    'Shanghai': [
        {
            'university': 'Fudan University (FDU)',
            'location': 'Center 212',
            'time': '2017 Oct 15th, 2:30 pm',
            'mapid': 'loc3'
        },
        {
            'university': 'Shanghai Jiaotong University (SJTU)',
            'location': 'Center 212',
            'time': '2017 Oct 15th, 2:30 pm',
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
