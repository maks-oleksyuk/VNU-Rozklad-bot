import json
import requests
from pathlib import Path
from datetime import datetime


async def getFaculties():
    path = Path("json/faculties.json")
    if not path.exists() or datetime.now().day == 31:
        payload = {
            "req_type": "obj_list",
            "req_mode": "group",
            "req_format": "json",
            "coding_mode": "UTF8",
            "bs": "ok",
        }
        r = requests.get(
            "http://194.44.187.20/cgi-bin/timetable_export.cgi", params=payload
        )
        text = json.loads(r.text)
        if text["psrozklad_export"]["code"] == "0":
            with open("json/faculties.json", "w+") as f:
                json.dump(text, f, sort_keys=True, indent=2, ensure_ascii=False)
