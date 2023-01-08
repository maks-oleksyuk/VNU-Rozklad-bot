import json
from datetime import datetime
from pathlib import Path

import requests

api_url = 'http://194.44.187.20/cgi-bin/timetable_export.cgi'


async def get_chair():
    """Obtaining and preserving department data"""
    path = Path("./../json/chair.min.json")
    if not path.exists() or datetime.now().day == 1:
        payload = {
            'req_type': 'obj_list',
            'req_mode': 'teacher',
            'show_ID': 'yes',
            'req_format': 'json',
            'coding_mode': 'UTF8',
            'bs': 'ok',
        }
        res = requests.get(api_url, params=payload)
        text = json.loads(res.text)
        index = []
        for d in range(len(text['psrozklad_export']['departments'])):
            for g in range(len(text['psrozklad_export']['departments'][d]['objects'])):
                n = text['psrozklad_export']['departments'][d]['objects'][g]
                if n['name'].find('....') != -1 or n['name'].find('Вакансія') != -1:
                    index.append([d, g])
                if n['B'].find('.') != -1:
                    n['B'] = ''
        for i in reversed(index):
            del text['psrozklad_export']['departments'][i[0]]['objects'][i[1]]
        if text['psrozklad_export']['code'] == '0':
            with open('./../json/chair.min.json', 'w+') as f:
                json.dump(text, f, ensure_ascii=False)


async def get_faculties():
    """Obtaining and saving data about faculties"""
    path = Path('./..json/faculties.min.json')
    if not path.exists() or datetime.now().day == 1:
        payload = {
            'req_type': 'obj_list',
            'req_mode': 'group',
            'show_ID': 'yes',
            'req_format': 'json',
            'coding_mode': 'UTF8',
            'bs': 'ok',
        }
        r = requests.get(api_url, params=payload)
        text = json.loads(r.text)
        if text['psrozklad_export']['code'] == '0':
            with open('./../json/faculties.min.json', 'w+') as f:
                json.dump(text, f, ensure_ascii=False)
