from datetime import date, timedelta
from urllib.parse import urlencode

import aiohttp


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
            async with aiohttp.ClientSession() as session:
                async with session.get(self._api_url, params=payload) as res:
                    text = await res.json()
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
            async with aiohttp.ClientSession() as session:
                async with session.get(self._api_url, params=payload) as res:
                    text = await res.json()
                    code = text['psrozklad_export']['code']
                    if code == '0':
                        await self._db.save_teachers(
                            text['psrozklad_export']['departments'])
                    else:
                        error = text['psrozklad_export']['error']['error_message']
                        raise Exception(f'Request return bad response code - {code}: {error}')
        except Exception as e:
            self.log.error(f'API Error: {e}; Table teachers not updated!')

    async def get_audiences(self) -> dict | None:
        """Sends a GET request to the API and returns a dictionary with audiences or None.

        Returns:
            A dictionary with audiences or None if the request was unsuccessful.
        Raises:
            Exception: If the request return a bad response code.
        """
        payload = {
            'req_type': 'obj_list',
            'req_mode': 'room',
            'show_ID': 'yes',
            'req_format': 'json',
            'coding_mode': 'UTF8',
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._api_url, params=payload) as res:
                    text = await res.json()
                    code = text['psrozklad_export']['code']
                    if code == '0':
                        return text['psrozklad_export']['blocks']
                    else:
                        error = text['psrozklad_export']['error']['error_message']
                        raise Exception(f'Request return bad response code - {code}: {error}')
        except Exception as e:
            self.log.error(f'API Error: {e}')
            return None

    async def get_free_rooms(self,
                             date: date = date.today(),
                             lesson: int = -1,
                             block: str = '',
                             type: str = '') -> dict | None:
        """Returns a list of free rooms for a given date, lesson, block and type.

        Args:
            date (optional): Date for which to get free rooms. Defaults to today.
            lesson (optional): Lesson number for which to get free rooms. Defaults to -1.
            block (optional): Block name for which to get free rooms. Defaults to ''.
            type (optional): Type of room for which to get free rooms. Defaults to ''.

        Returns:
            dict or None: A dictionary containing free rooms information for a given
            date, lesson, block and type or None if an error occurred.

        Raises:
            Exception: If the request returns a bad response code.
        """
        payload = {
            'req_type': 'free_rooms_list',
            'rooms_date': date.strftime('%d.%m.%Y'),
            'lesson': lesson,
            'block_name': block,
            'room_type': type,
            'req_format': 'json',
            'coding_mode': 'windows-1251',
        }
        # We change the encoding due to the peculiarities of the server.
        payload = urlencode(payload, encoding='windows-1251')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self._api_url}?{payload}') as res:
                    text = await res.json(encoding='windows-1251')
                    code = text['psrozklad_export']['code']
                    if code != '0':
                        error = text['psrozklad_export']['error']['error_message']
                        raise Exception(f'Request return bad response code - {code}: {error}')
                    return text['psrozklad_export']['free_rooms'][0]['rooms']
        except Exception as e:
            self.log.error(f'API Error: {e}')
            return None

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
            async with aiohttp.ClientSession() as session:
                async with session.get(self._api_url, params=payload) as res:
                    text = await res.json()
                    code = text['psrozklad_export']['code']
                    # If the answer is successful, we update the data in the database.
                    if code == '0':
                        data = text['psrozklad_export']['roz_items']
                        await self._db.save_timetable(id, mode, data, s_date, e_date)
                    else:
                        error = text['psrozklad_export']['error']['error_message']
                        raise Exception(f'Request return bad response code - {code}\n{error}')
        except Exception as e:
            self.log.error(f'API Error: {e}')
