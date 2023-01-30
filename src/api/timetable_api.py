import json
from datetime import date, timedelta

import requests
from database.db import save_groups, save_teachers

api_url = 'http://94.130.69.82/cgi-bin/timetable_export.cgi'


async def get_groups():
    """ Obtaining and saving data about groups """
    payload = {
        'req_type': 'obj_list',
        'req_mode': 'group',
        'show_ID': 'yes',
        'req_format': 'json',
        'coding_mode': 'UTF8',
    }
    try:
        res = requests.get(api_url, params=payload)
        text = json.loads(res.text)
        code = text['psrozklad_export']['code']
        if code == '0':
            await save_groups(text['psrozklad_export']['departments'])
        else:
            error = text['psrozklad_export']['error']['error_message']
            raise Exception(
                f'Request return bad response code - {code}\n{error}')
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
    }
    try:
        res = requests.get(api_url, params=payload)
        text = json.loads(res.text)
        code = text['psrozklad_export']['code']
        if code == '0':
            await save_teachers(text['psrozklad_export']['departments'])
        else:
            error = text['psrozklad_export']['error']['error_message']
            raise Exception(
                f'Request return bad response code - {code}\n{error}')
    except Exception as e:
        print(f'API Error: {e}\nTable teachers not updated!')


async def get_timetable(id, mode,
                        s_date=date.today().strftime('%d.%m.%Y'),
                        e_date=(date.today() + timedelta(weeks=2))
                        .strftime('%d.%m.%Y')):
    payload = {
        'req_type': 'rozklad',
        'req_mode': mode,
        'OBJ_ID': id,
        'ros_text': 'separated',
        'begin_date': s_date,
        'end_date': e_date,
        'req_format': 'json',
        'coding_mode': 'UTF8',
    }
    try:
        res = requests.get(api_url, params=payload)
        text = json.loads(res.text)
        code = text['psrozklad_export']['code']
        if code == '0':
            pass
            # await save_teachers(text['psrozklad_export']['departments'])
        else:
            error = text['psrozklad_export']['error']['error_message']
            raise Exception(
                f'Request return bad response code - {code}\n{error}')
    except Exception as e:
        print(f'API Error: {e}')
