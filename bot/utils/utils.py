from datetime import datetime


async def is_date(date_string):
    formats = ['%d.%m', '%d/%m', '%d-%m',
               '%m.%d', '%m/%d', '%m-%d',
               '%d.%m.%y', '%d/%m/%y', '%d-%m-%y',
               '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y']
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_string, fmt)
            if date_obj.year == 1900:
                date_obj = date_obj.replace(year=datetime.now().year)
            return date_obj
        except ValueError:
            pass
    else:
        return False
