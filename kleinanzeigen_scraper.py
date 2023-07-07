import asyncio
import time
import pytz
from bs4 import BeautifulSoup
import requests
import datetime


async def getHTMLdocument(url, loop):
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "cookie": "AHWqTUlhftkLIuXSbIVa5uKh77iLa_kw1Tx9rkm3xTMos06ERQq3MgXWSdg7-iCp9WA"
    }
    response = await loop.run_in_executor(None, lambda: requests.get(url, headers=headers))
    return response.text


async def get_data_adids(html_document):
    bs_4 = BeautifulSoup(html_document, "lxml")
    html_list_of_adds = bs_4.find(id="srchrslt-adtable")
    list_of_adds = html_list_of_adds.find_all(class_="ad-listitem lazyload-item")

    x = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
    data_adids = []
    dict_1 = {}
    for i in list_of_adds:

        time = i.find(class_="aditem-main--top--right")

        unic_id = i.find(class_="aditem")["data-adid"]
        try:
            text_time = i.find(class_="ellipsis")["href"]
        except:
            text_time = "None"
        try:
            price = i.find(class_="aditem-main--middle--price-shipping--price")
            price = price.get_text()
            price = price.strip()
        except:
            price = "None"
        try:
            location = i.find(class_="aditem-main--top--left")
            location = location.get_text()
            location = location.strip()
        except:
            location = "None"
        try:
            description = i.find(class_="aditem-main--middle--description")
            description = description.get_text()
            description = description.strip()
        except:
            description = "None"

        try:
            note = i.find(class_="text-module-end")
            note = note.get_text()
            note = note.strip()
        except:
            note = "None"

        try:
            text = i.find(class_="ellipsis")
            text = text.get_text()
            text = text.strip()
        except:
            text = "None"

        time = (time.get_text()).strip()
        time = time.split(", ")[1]
        if len(time.split(":")[0]) == 1:
            time = "0" + time
        item_time = datetime.datetime.strptime(time, "%H:%M").time()
        time_diff = datetime.datetime.combine(datetime.date.today(), x.time()) - datetime.datetime.combine(
            datetime.date.today(), item_time)
        time_diff_minutes = time_diff.seconds // 60
        if time_diff_minutes == 1 or time_diff_minutes == 2 or time_diff_minutes == 3:
            dict_1[unic_id] = {"link": "https://www.kleinanzeigen.de/" + text_time, "time": time, "price": price, "location":location, "description":description, "note":note, "text":text}
            data_adids.append(unic_id)
        else:
            pass
    return data_adids, dict_1


async def process_link(link, loop):
    previos_link = [] # Big collect
    big_dict = {}
    i2 = 0
    while True:
        html_document = await getHTMLdocument(link, loop)
        list_1, dict_1 = await get_data_adids(html_document)
        for i in list_1:
            if i not in previos_link:
                previos_link.append(i)
                big_dict[i] = dict_1[i]
        if i2 == 12:


            for i in big_dict:
                print("—------")
                print(f'ID:{i}')
                print(f'Link: {big_dict[i]["link"]}')
                print(f'Time and price: {big_dict[i]["time"], big_dict[i]["price"]}')
                print(f'Text: {big_dict[i]["text"]}')
                print(f'Description: {big_dict[i]["description"]}')
                print(f'{big_dict[i]["note"]}')
                print(f'{big_dict[i]["location"]}')

            big_dict = {}
            i2 = 0
        print(i2, " - ", link)
        i2 += 1
        await asyncio.sleep(10)


async def main(link_list, loop):
    tasks = [process_link(link, loop) for link in link_list]
    await asyncio.gather(*tasks)


async def loop_scraper_start(link_list):
    loop = asyncio.get_event_loop()
    try:
        await main(link_list, loop)
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            pass  # Ignore the error if the event loop is already running
        else:
            raise  # Reraise the error if it's a different RuntimeError
    finally:
        if loop.is_running():
            loop.stop()
            await loop.shutdown_asyncgens()
        loop.close()

async def loop_loops(user_id):
    while True:
        print(user_id)
        await asyncio.sleep(1)

# loop_scraper_start(["https://www.kleinanzeigen.de/s-berlin/bmw/k0l3331", "https://www.kleinanzeigen.de/s-berlin/apple/k0l3331", "https://www.kleinanzeigen.de/s-lego/k0"])