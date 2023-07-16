import pytz
from aiogram.types import ParseMode
from bs4 import BeautifulSoup
import requests
import datetime
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from Bot_Folder.data_base import connection


async def get_html_document(url, loop_variable):
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "cookie": "AHWqTUlhftkLIuXSbIVa5uKh77iLa_kw1Tx9rkm3xTMos06ERQq3MgXWSdg7-iCp9WA"
    }
    response = await loop_variable.run_in_executor(None, lambda: requests.get(url, headers=headers))
    status_connection = response.status_code

    if status_connection == 200:
        return response.text
    else:
        return 300


async def get_data_adids(html_document):
    bs_4 = BeautifulSoup(html_document, "lxml")
    try:
        html_list_of_adds = bs_4.find(id="srchrslt-adtable")
        list_of_adds = html_list_of_adds.find_all(class_="ad-listitem lazyload-item")
    except:
        print("There was a no post at all - ", end="")
        return [], {}
    x = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
    data_adids = []
    dict_1 = {}
    for i in list_of_adds:

        time = i.find(class_="aditem-main--top--right")

        unic_id = i.find(class_="aditem")["data-adid"]
        try:
            text_time = i.find(class_="ellipsis")["href"]
        except:
            text_time = "No time"
        try:
            price = i.find(class_="aditem-main--middle--price-shipping--price")
            price = price.get_text()
            price = price.strip()
        except:
            price = "No Preis"
        try:
            location = i.find(class_="aditem-main--top--left")
            location = location.get_text()
            location = location.strip()
            location = "".join(line.lstrip() for line in location.split("\n"))

        except:
            location = "No Ort"
        try:
            description = i.find(class_="aditem-main--middle--description")
            description = description.get_text()
            description = description.strip()
        except:
            description = "No Beschreibung"

        try:
            note = i.find(class_="text-module-end")
            note = note.get_text()
            note = note.strip()
            if note == "":
                note = "No note"

        except:
            note = "No note"

        try:
            text = i.find(class_="ellipsis")
            text = text.get_text()
            text = text.strip()
        except:
            text = "No text"

        time = (time.get_text()).strip()
        try:
            time_day = time.split(", ")[0]
            if time_day == "Heute":
                time = time.split(", ")[1]
                if len(time.split(":")[0]) == 1:
                    time = "0" + time
                item_time = datetime.datetime.strptime(time, "%H:%M").time()
                time_diff = datetime.datetime.combine(datetime.date.today(), x.time()) - datetime.datetime.combine(
                    datetime.date.today(), item_time)
                time_diff_minutes = time_diff.seconds // 60
                if time_diff_minutes == 1 or time_diff_minutes == 2 or time_diff_minutes == 3:
                    dict_1[unic_id] = {"link": "https://www.kleinanzeigen.de" + text_time, "time": time, "price": price, "location": location, "description": description,
                                       "note": note, "text": text}
                    data_adids.append(unic_id)
        except:
            pass
        else:
            pass
    return data_adids, dict_1


async def process_link(link, loop_variable, user_id):
    previous_link = []  # Big collect
    big_dict = {}
    i2 = 0
    while True:
        try:
            html_document = await get_html_document(link, loop_variable)
            if html_document == 300:
                print("No connection")
            else:
                list_1, dict_1 = await get_data_adids(html_document)
                for i in list_1:
                    if i not in previous_link:
                        previous_link.append(i)
                        big_dict[i] = dict_1[i]

                if i2 == 6:  # Fast setting
                    for i in big_dict:
                        message_for_user = ""
                        print(i, big_dict[i]["link"])

                        message_for_user += f'<a href="{big_dict[i]["link"]}">{big_dict[i]["text"]} ist neu auf Kleinanzeigen‼</a>\n\n'
                        message_for_user += f'🛒 Preis: {big_dict[i]["price"]}\n'
                        message_for_user += f'📍 Ort: {big_dict[i]["location"]}\n\n'
                        message_for_user += f'🔍 Details: {big_dict[i]["note"]}\n'
                        message_for_user += f'📝 Beschreibung: {big_dict[i]["description"]}\n'
                        message_for_user += f'Time: {big_dict[i]["time"]}\n'

                        await send_message_to_user(user_id, message_for_user)

                    big_dict = {}
                    i2 = 0

        except Exception as es:
            print("Bad connection with site or problem with link!")

        print("Iteration count - ", i2, ". For user:", user_id, " - ", link)

        i2 += 1
        await asyncio.sleep(15)  # Fast setting


async def main_scrape(link_list, loop_variable, user_id):
    tasks = [process_link(link, loop_variable, user_id) for link in link_list]
    await asyncio.gather(*tasks)



async def loop_scraper_start(link_list, user_id):
    loop_veriable = asyncio.get_event_loop()
    try:
        await main_scrape(link_list, loop_veriable, user_id)
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            pass  # Ignore the error if the event loop is already running
        else:
            raise  # Reraise the error if it's a different RuntimeError
    finally:
        if loop_veriable.is_running():
            loop_veriable.stop()
            await loop_veriable.shutdown_asyncgens()
        loop_veriable.close()


async def test_db():
    list_of_lost = [["", "", "710680274", "", "", "", "https://www.kleinanzeigen.de/s-tiptoi/k0"],
                    ["", "", "710680274", "", "", "", "https://www.ebay-kleinanzeigen.de/s-preis::700/49-zoll-monitor/k0", ],
                    ["", "", "710680274", "", "", "", "https://www.ebay-kleinanzeigen.de/s-wii-spielesammlung/k0", ],
                    ["", "", "710680274", "", "", "", "https://www.ebay-kleinanzeigen.de/s-nintendo-3ds-pokemon/k0", ],
                    ["", "", "710680274", "", "", "", "https://www.ebay-kleinanzeigen.de/s-fire-emblem-fates-3ds/k0", ],
                    ["", "", "710680274", "", "", "", "https://www.ebay-kleinanzeigen.de/s-quickborn/schrebergarten/k0l769", ],
                    ["", "", "710680274", "", "", "", "https://www.ebay-kleinanzeigen.de/s-garage-lagerraum/quickborn/preis::60/wohnmobil-stellplatz/k0c197l769r10", ],
                    ["", "", "710680274", "", "", "", "https://www.kleinanzeigen.de/s-new-nintendo-2ds-xl/k0", ],

                    ]

    return list_of_lost


async def function_1(results):
    user_links_list = {}
    for row in results:
        logged_user_id = row[2]  # 6
        link = row[6]  # 3
        if logged_user_id not in user_links_list:
            user_links_list[logged_user_id] = [link]
        else:
            user_links_list[logged_user_id].append(link)
    return user_links_list


async def send_message_to_user(user_id, message):
    bot_token = ''
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=user_id, text=message)


async def main():
    while True:
        new_user_links = await test_db()
        dict_of_users = await function_1(new_user_links)

        for user_id in dict_of_users:
            await send_message_to_user(user_id, "Hello, i am testing now a new version of scraper and you was in db)")
        print("Lol")
        try:
            tasks = []
            for user_id in dict_of_users:
                print(user_id)
                tasks.append(loop.create_task(loop_scraper_start(dict_of_users[user_id], user_id)))

            # Wait for all tasks to complete
            await asyncio.wait(tasks)

        except:
            print("No chat")

        await asyncio.sleep(15)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
