import json

import requests
from database.db import save_groups

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
    # try:
    #     res = requests.get(api_url, params=payload)
    #     text = json.loads(res.text)
    # except Exception as e:
    with open('./../json/faculty.min.json') as f:
        text = json.loads(f.read())
        if text['psrozklad_export']['code'] == '0':
            await save_groups(text['psrozklad_export']['departments'])
    # print(f'API Error: {e}')


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
    except Exception as e:
        print(f'API Error: {e}')
    # index = []
# for d in range(len(text['psrozklad_export']['departments'])):
#     for g in range(len(
#             text['psrozklad_export']['departments'][d]['objects'])):
#         n = text['psrozklad_export']['departments'][d]['objects'][g]
#         if n['name'].find('....') != -1 or n['name'].find(
#                 'Вакансія') != -1:
#             index.append([d, g])
#         if n['B'].find('.') != -1:
#             n['B'] = ''
# for i in reversed(index):
#     del text['psrozklad_export']['departments'][i[0]]['objects'][i[1]]
# if text['psrozklad_export']['code'] == '0':
#     with open('./../json/chair.min.json', 'w+') as f:
#         json.dump(text, f, ensure_ascii=False)
