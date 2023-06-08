from datetime import datetime
import random
import time

import requests
from bs4 import BeautifulSoup
from notify_run import Notify

URL = 'https://www.passaportonline.poliziadistato.it/GestioneDisponibilitaAction.do?codop=getDisponibilitaCittadino'
COOKIES = {
    'AGPID':'AHwhZZoLxwoCjfwyLd87AA$$',
    'AGPID_FE':'A4h1AygKxwoWRZ91RbMVOQ$$',
    'JSESSIONID': 'omPc-GGhOG02fTj5gUvzyDwy'
}

REFRESH_MINS = (15, 20)
MAX_DATE = '2023-11-21'
DESIRED_LOCATIONS=["Commissariato Gallarate","Questura di Varese","Commissariato Busto Arsizio"]


def extract_first_date(soup: BeautifulSoup):
    table = soup.find('table', attrs={'class': 'naviga_disponibilita'})
    date = table.findAll('td')[1].getText(strip=True)
    return date
def extract_location(soup:BeautifulSoup):
    td_tag = soup.select_one('td[headers="descrizione"]')
    if td_tag is not None:
        a_tag = td_tag.find('a')
        if a_tag is not None:
            text = a_tag.text.strip()
            return text
def get_link_for_next_availability(soup:BeautifulSoup):
    td_tag = soup.select_one('td.dopo')  
    if td_tag is not None:  
        a_tag = td_tag.find('a')  
        if a_tag is not None: 
            return a_tag.get('href')
    raise Exception("NextDayNotAvailable")

def wait():
    sleep_mins = random.uniform(REFRESH_MINS[0], REFRESH_MINS[1])
    print(f'Sleeping {sleep_mins} minutes')
    time.sleep(sleep_mins * 60)


def acceptable(date) -> bool:
    return date <= MAX_DATE


def start(notify: Notify):
    localurl = URL
    while True:
        date = "2030-01-01"
        location = ""
        while True:
            req = requests.get(localurl, cookies=COOKIES)
            soup = BeautifulSoup(req.content, "html.parser")
            date = extract_first_date(soup)
            location = extract_location(soup)
            if location in DESIRED_LOCATIONS:
                break
            localurl = "https://www.passaportonline.poliziadistato.it/"+get_link_for_next_availability(soup)
            time.sleep(2)
        if acceptable(date):
            date_object = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
            notify.send(f'Appointment available the {date_object.strftime("%d.%m.%Y")} at {location}')
        wait()
def main():
    notify = Notify()
    try:
        start(notify)
    except:
        print('An exception occurred')
        notify.send('An exception occurred')
if __name__ == '__main__':
    main()
