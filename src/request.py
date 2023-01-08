import json
from datetime import datetime, timedelta
from pathlib import Path

import requests


async def get_schedule(id, mode, date=None):
    """Getting schedule data

    Args:
        id (int): Schedule ID
        mode (str): Schedule mode
        date (datetime): The date on which you need to get the schedule

    Returns:
        dict: Received information
    """
    ND = datetime.now()
    NW = datetime.now().weekday()
    if date:
        begin_date = date.strftime("%d.%m.%Y")
        end_date = date.strftime("%d.%m.%Y")
    else:
        begin_date = (ND - timedelta(days=NW)).strftime("%d.%m.%Y")
        end_date = (ND + timedelta(days=13 - NW)).strftime("%d.%m.%Y")
    payload = {
        "req_type": "rozklad",
        "req_mode": mode,
        "OBJ_ID": id,
        "ros_text": "separated",
        "show_empty": "yes",
        "begin_date": begin_date,
        "end_date": end_date,
        "req_format": "json",
        "coding_mode": "UTF8",
        "bs": "ok",
    }
    r = requests.get(
        "http://194.44.187.20/cgi-bin/timetable_export.cgi", params=payload
    )
    text = json.loads(r.text)
    return text
