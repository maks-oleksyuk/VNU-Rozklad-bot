import json
import requests
from pathlib import Path
from datetime import datetime, timedelta


async def getFaculties():
    path = Path("json/faculties.min.json")
    if not path.exists() or datetime.now().day == 31:
        payload = {
            "req_type": "obj_list",
            "req_mode": "group",
            "show_ID": "yes",
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
            with open("json/faculties.min.json", "w+") as f:
                json.dump(text, f, ensure_ascii=False)


async def getChair():
    path = Path("json/chair.min.json")
    if not path.exists() or datetime.now().day == 31:
        payload = {
            "req_type": "obj_list",
            "req_mode": "teacher",
            "show_ID": "yes",
            "req_format": "json",
            "coding_mode": "UTF8",
            "bs": "ok",
        }
        r = requests.get(
            "http://194.44.187.20/cgi-bin/timetable_export.cgi", params=payload
        )
        text = json.loads(r.text)
        index = []
        for d in range(len(text["psrozklad_export"]["departments"])):
            for g in range(len(text["psrozklad_export"]["departments"][d]["objects"])):
                n = text["psrozklad_export"]["departments"][d]["objects"][g]
                if n["name"].find("....") != -1 or n["name"].find("Вакансія") != -1:
                    index.append([d, g])
                if n["B"].find(".") != -1:
                    n["B"] = ""
        for i in reversed(index):
            del text["psrozklad_export"]["departments"][i[0]]["objects"][i[1]]
        if text["psrozklad_export"]["code"] == "0":
            with open("json/chair.json", "w+") as f:
                json.dump(text, f, sort_keys=True, indent=2, ensure_ascii=False)
            with open("json/chair.min.json", "w+") as f:
                json.dump(text, f, ensure_ascii=False)


async def get_schedule(id, mode, date):
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
