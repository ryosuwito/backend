# -*- coding: utf-8 -*-
import json

from django.core.management.base import BaseCommand

from chinaevent.models import EventContent


CHINA_EVENT_CONTENT = {
    '2020': {
        "writtenTests":
        [
            {
                "university": "北京大学",
                "location": "待定",
                "time": "2019年10月19日, 09:00 - 12:00"
            },
            {
                "university": "复旦大学",
                "location": "待定",
                "time": "2019年10月19日, 09:00 - 12:00"
            },
            {
                "university": "上海交通大学",
                "location": "待定",
                "time": "2019年10月19日, 09:00 - 12:00"
            }
        ],
        "careerTalks":
        [
            {
                "university": "北京大学宣讲会",
                "location": "英杰交流中心第二会议室",
                "time": "2019年10月16日, 19:00 - 21:00",
                "mapid": "loc1"
            },
            {
                "university": "清华大学交流会",
                "location": "待定",
                "time": "待定",
                "mapid": "loc2"
            },
            {
                "university": "复旦大学宣讲会",
                "location": "待定",
                "time": "待定",
                "mapid": "loc3"
            },
            {
                "university": "上海交通大学宣讲会",
                "location": "待定",
                "time": "待定",
                "mapid": "loc4"
            }
        ]
    }
}


class Command(BaseCommand):
    help = 'Add china event content'

    def handle(self, *args, **options):
        for year, content_dict in CHINA_EVENT_CONTENT.items():
            cnt = EventContent.objects.filter(year=year).count()
            if cnt > 0:
                self.stdout.write(self.style.WARNING('The content of the year {} is already exist'.format(year)))
                continue

            try:
                event_content = EventContent(year=year, payload=json.dumps(content_dict, ensure_ascii=False, encoding='utf-8'))
                event_content.save()
            except Exception as err:
                self.stdout.write(self.style.ERROR(err))
            else:
                self.stdout.write(self.style.SUCCESS('The content of the year {} has added successfully!'.format(year)))
