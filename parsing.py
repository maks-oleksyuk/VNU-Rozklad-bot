import datetime
import keyboard
import variables
from bs4 import BeautifulSoup


# Парсинг по сторінці та формування стрічки
def parsing(req, mes, date):
    # Створення змінних для парсингу
    soup = BeautifulSoup(req.text, "html.parser")
    h4 = soup.select(".col-md-6 > h4")
    table = soup.find_all("table")
    td = soup.findAll("td")

    # n - кількість пар для відображення (можуть бути вікна), b - наявність розкладу
    b = False
    n = len(td) / len(table) / 3

    # Перевірка наявності дати введеної користувачем
    if date:
        if type(date) == datetime.date:
            d = date
        else:
            d = datetime.datetime.strptime(date, "%d.%m.%y").date()
    else:
        d = datetime.date.today()

    if variables.last_selec[mes.from_user.id] == 1:
        subtitle = soup.find_all(attrs={"id": "group"})
        who = "групи"
        icons = "🎓"

    elif variables.last_selec[mes.from_user.id] == 2:
        subtitle = soup.find_all(attrs={"id": "teacher"})
        who = "викладача"
        icons = "💼"

    # Формування заголовку розкладу
    str = (
        icons
        + "<b> Розклад "
        + who
        + "<u> "
        + subtitle[0]["value"]
        + "</u>\n🔹 на "
        + d.strftime("%d.%m.%Y")
        + " ("
        + variables.week[d.weekday()]
        + ")</b>\n"
    )

    # Формування стрічки розкладу для показу
    for w in h4:
        if d.strftime("%d.%m.%Y") in w.text:
            index_start = 3 * n * h4.index(w)
            for i in range(int(index_start), int(index_start + n * 3), 3):
                if not bool(td[i + 2].text.strip()):
                    continue
                else:
                    str_numtime = (
                        "\n<i>🔅 "
                        + td[i].text
                        + " Пара ("
                        + td[i + 1].text[:5]
                        + " - "
                        + td[i + 1].text[5:]
                        + ")</i>\n"
                    )
                    for br in td[i + 2]("br"):
                        br.replace_with("\n")
                    if len(td[i + 2]("div")) == 2:
                        str_couple = (
                            td[i + 2]
                            .text.replace("\n  ", "\n")
                            .replace("\n ", "\n")
                            .replace("\n", "</u></b>\n", 5)
                            .replace("</u></b>\n", "\n", 4)
                            .replace("\n", "<b><u>\n", 4)
                            .replace("<b><u>\n", "\n", 3)
                            .replace("\n", "</u></b>\n", 1)
                        )
                    else:
                        str_couple = (
                            td[i + 2]
                            .text.replace("\n  ", "\n")
                            .replace("\n ", "\n")
                            .replace("\n", "</u></b>\n", 1)
                        )
                    str += str_numtime + "<b><u>" + str_couple

            # міняємо зміну b, та відправляємо розклад
            b = True
            variables.bot.send_message(
                mes.from_user.id,
                str,
                parse_mode="html",
                reply_markup=keyboard.set_markup(mes.from_user.id, 3),
            )

    # Якщо розкладу не знайдено виводимо альтернативне повідомлення
    if not b:
        variables.bot.send_message(
            mes.from_user.id,
            str + "<b>\nВітаю,  в  тебе  вихідний!🎉😎</b>",
            parse_mode="html",
            reply_markup=keyboard.set_markup(mes.from_user.id, 3),
        )

    # log
    print(
        len(variables.last_selec),
        mes.from_user.id,
        mes.from_user.full_name,
        mes.from_user.username,
        d,
        mes.text,
    )
