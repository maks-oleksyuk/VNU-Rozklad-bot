import json
from datetime import date, timedelta

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

    async def get_schedule(self, id: int, mode: str, s_date=date.today(),
                           e_date=date.today() + timedelta(weeks=2)) -> None:
        """Get schedule data from API for specified ID and mode, then saves it to database.

        Args:
            id: ID of the schedule.
            mode: Mode of the schedule ('teacher', or 'group').
            s_date: Start date of the schedule. Default is today.
            e_date: End date of the schedule. Default is 2 weeks after s_date.

        Raises:
            Exception: If the API returns a bad response code.
        """
        payload = {
            'req_type': 'rozklad',
            'req_mode': mode,
            'OBJ_ID': id,
            'ros_text': 'separated',
            'begin_date': s_date.strftime('%d.%m.%Y'),
            'end_date': e_date.strftime('%d.%m.%Y'),
            'req_format': 'json',
            'coding_mode': 'UTF8',
        }
        try:
            res = requests.get(self._api_url, params=payload)
            text = json.loads(res.text)
            code = text['psrozklad_export']['code']
            # If the answer is successful, we update the data in the database.
            if code == '0':
                data = text['psrozklad_export']['roz_items']
                await self._db.save_timetable(id, mode, data, s_date, e_date)
            else:
                error = text['psrozklad_export']['error']['error_message']
                raise Exception(
                    f'Request return bad response code - {code}\n{error}')
        except Exception as e:
            self.log.error(f'API Error: {e}')
