import re
from datetime import datetime


async def is_date(date_str):
    """Check if a string is a valid date in various formats.

    Args:
        date_str: string to check if it is a valid date in any of the formats.

    Returns:
        datetime object if the string is a valid date, else False.

    Example:
        is_date('22.02.2022') => datetime.datetime(2022, 2, 22, 0, 0).
    """
    formats = ['%d.%m', '%d/%m', '%d-%m',
               '%m.%d', '%m/%d', '%m-%d',
               '%d.%m.%y', '%d/%m/%y', '%d-%m-%y',
               '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y']
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            if date_obj.year == 1900:
                date_obj = date_obj.replace(year=datetime.now().year)
            return date_obj
        except ValueError:
            pass
    else:
        return False


async def add_over_room(data: dict) -> dict:
    """Extracts and adds over value to a given room data dictionary.

    Args:
        data: A dictionary containing room data.

    Returns:
        A dictionary containing updated room data with added over value.
    """
    for room in data:
        match = re.search(r'ауд\. [A-ZА-Я]-(\d{1,3})', room['name'])
        room['floor'] = 1 \
            if match and len(match.group(1)) == 1 \
            else int(str(match.group(1))[0]) \
            if match else None
    return data


async def add_missing_type(data: dict) -> dict:
    for room in data:
        match = re.search(r'ауд\. Сектор(\d)', room['name'])
        if match:
            room['type'] = 'спорт'
    return data
