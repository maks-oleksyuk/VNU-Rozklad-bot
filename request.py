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


async def getChair():
    path = Path("json/chair.json")
    if not path.exists() or datetime.now().day == 31:
        payload = {
            "req_type": "obj_list",
            "req_mode": "teacher",
            "req_format": "json",
            "coding_mode": "UTF8",
            "bs": "ok",
        }
        r = requests.get(
            "http://194.44.187.20/cgi-bin/timetable_export.cgi", params=payload
        )
        text = json.loads(r.text)
        index = []
        for d in range(len(text["psrozklad_export"]["departments"]) - 1, -1, -1):
            for g in range(
                len(text["psrozklad_export"]["departments"][d]["objects"]) - 1, -1, -1
            ):
                n = text["psrozklad_export"]["departments"][d]["objects"][g]["name"]
                if (
                    n.find("Інфекціоніст") != -1
                    or n.find("Онколог") != -1
                    or n.find("Психіатр") != -1
                    or n.find("Фтизіатр") != -1
                    or n.find("Резерв") != -1
                    or n.find("Вакансія") != -1
                ):
                    index.append([d, g])
        for i in index:
            del text["psrozklad_export"]["departments"][i[0]]["objects"][i[1]]
        if text["psrozklad_export"]["code"] == "0":
            with open("json/chair.json", "w+") as f:
                json.dump(text, f, sort_keys=True, indent=2, ensure_ascii=False)
