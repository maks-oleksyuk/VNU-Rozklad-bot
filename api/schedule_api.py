import json

import requests


class ScheduleAPI:
    def __init__(self, api_ip: str):
        from loader import db, logger
        self._api_url = f'http://{api_ip}/cgi-bin/timetable_export.cgi'
        self.log = logger
        self._db = db

    async def get_groups(self):
        """ Obtaining and saving data about groups """
        payload = {
            'req_type': 'obj_list',
            'req_mode': 'group',
            'show_ID': 'yes',
            'req_format': 'json',
            'coding_mode': 'UTF8',
        }
        try:
            res = requests.get(self._api_url, params=payload)
            text = json.loads(res.text)
            code = text['psrozklad_export']['code']
            if code == '0':
                await self._db.save_groups(
                    text['psrozklad_export']['departments'])
            else:
                error = text['psrozklad_export']['error']['error_message']
                raise Exception(f'Request return bad response code - {code}: {error}')
        except Exception as e:
            self.log.error(f'API Error: {e}; Table groups not updated!')

    async def get_teachers(self):
        """ Obtaining and saving data about teachers """
        payload = {
            'req_type': 'obj_list',
            'req_mode': 'teacher',
            'show_ID': 'yes',
            'req_format': 'json',
            'coding_mode': 'UTF8',
        }
        try:
            res = requests.get(self._api_url, params=payload)
            text = json.loads(res.text)
            code = text['psrozklad_export']['code']
            if code == '0':
                await self._db.save_teachers(
                    text['psrozklad_export']['departments'])
            else:
                error = text['psrozklad_export']['error']['error_message']
                raise Exception(
                    f'Request return bad response code - {code}: {error}')
        except Exception as e:
            self.log.error(f'API Error: {e}; Table teachers not updated!')
