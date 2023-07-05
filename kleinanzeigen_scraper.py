import time

import pytz
from bs4 import BeautifulSoup
import requests
import datetime

def getHTMLdocument(url):
    # request for HTML document of given URL
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "cookie": "AHWqTUlhftkLIuXSbIVa5uKh77iLa_kw1Tx9rkm3xTMos06ERQq3MgXWSdg7-iCp9WA"
    }
    response = requests.get(url, headers=headers)
    # response will be provided in JSON format
    return response.text

def get_data_adids(html_document):
    bs_4 = BeautifulSoup(html_document, "lxml")
    html_list_of_adds = bs_4.find(id="srchrslt-adtable")
    list_of_adds = html_list_of_adds.find_all(class_="ad-listitem lazyload-item")

    with open("test.html", "w", encoding="utf-8") as file:
        file.write(html_document)

    # Extract the "data-adid" attributes
    x = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
    data_adids = []
    dict_1 = {}
    for i in list_of_adds:
        time = i.find(class_="aditem-main--top--right")
        unic_id = i.find(class_ = "aditem")["data-adid"]
        try:
            text = i.find(class_= "ellipsis")["href"]
        except:
            text = "None"
        time = (time.get_text()).strip()
        time = time.split(", ")[1]  # Split the text by ", " and get the second part
        # If the time starts with a single-digit hour (e.g., "0:18"), add a leading zero
        if len(time.split(":")[0]) == 1:
            time = "0" + time

        # Convert the extracted time to a datetime object
        item_time = datetime.datetime.strptime(time, "%H:%M").time()

        # Calculate the time difference in minutes
        time_diff = datetime.datetime.combine(datetime.date.today(), x.time()) - datetime.datetime.combine(datetime.date.today(), item_time)
        time_diff_minutes = time_diff.seconds // 60
        if time_diff_minutes == 1 or time_diff_minutes == 2 or time_diff_minutes == 3:
            dict_1[unic_id] = {"link":"https://www.kleinanzeigen.de/"+ text, "time":time}
            data_adids.append(unic_id)
        else:
            pass

    return data_adids, dict_1

def main(link_list):
    for link in link_list:
        previos_link = []
        big_dict = {}

        i2 = 0
        while True:
            print(link)
            html_document = getHTMLdocument(link)
            list_1, dict_1 = get_data_adids(html_document)
            for i in list_1:
                if i not in previos_link:
                    previos_link.append(i)
                    big_dict[i] = dict_1[i]["link"]
            if i2 == 12:
                for i in big_dict:
                    print(i, big_dict[i])
                big_dict = {}
                i2 =0

            print(i2)
            i2 += 1
            time.sleep(10)
             # Refresh



if __name__ == '__main__':
    main(["https://www.kleinanzeigen.de/s-koeln/bmw/k0l945", 'https://www.kleinanzeigen.de/s-apple/k0'])