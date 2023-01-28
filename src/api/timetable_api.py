import json

import requests
from database.db import save_groups, save_teachers

api_url = 'http://194.44.187.20/cgi-bin/timetable_export.cgi'


async def get_groups():
    """ Obtaining and saving data about groups """
    payload = {
        'req_type': 'obj_list',
        'req_mode': 'group',
        'show_ID': 'yes',
        'req_format': 'json',
        'coding_mode': 'UTF8',
        'bs': 'ok',
    }
    try:
        res = requests.get(api_url, params=payload)
        text = json.loads(res.text)
        code = text['psrozklad_export']['code']
        if code == '0':
            await save_groups(text['psrozklad_export']['departments'])
        else:
            raise Exception(f'Request return bad response code - {code}')
    except Exception as e:
        print(f'API Error: {e}\nTable groups not updated!')


async def get_teachers():
    """ Obtaining and saving data about teachers """
    payload = {
        'req_type': 'obj_list',
        'req_mode': 'teacher',
        'show_ID': 'yes',
        'req_format': 'json',
        'coding_mode': 'UTF8',
        'bs': 'ok',
    }
    try:
        res = requests.get(api_url, params=payload)
        text = json.loads(res.text)
        code = text['psrozklad_export']['code']
        if code == '0':
            await save_teachers(text['psrozklad_export']['departments'])
        else:
            raise Exception(f'Request return bad response code - {code}')
    except Exception as e:
        print(f'API Error: {e}\nTable teachers not updated!')
