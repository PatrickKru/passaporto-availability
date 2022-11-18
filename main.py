import random
import time

import requests
from bs4 import BeautifulSoup
from notify_run import Notify

URL = 'https://www.passaportonline.poliziadistato.it/GestioneDisponibilitaAction.do?codop=getDisponibilitaCittadino'
COOKIES = {
    'JSESSIONID': 'SESSION_ID'
}

REFRESH_MINS = (15, 20)
MAX_DATE = '2023-01-25'


def extract_first_date(soup: BeautifulSoup):
    table = soup.find('table', attrs={'class': 'naviga_disponibilita'})
    date = table.findAll('td')[1].getText(strip=True)

    return date


def wait():
    sleep_mins = random.uniform(REFRESH_MINS[0], REFRESH_MINS[1])
    print(f'Sleeping {sleep_mins} minutes')
    time.sleep(sleep_mins * 60)


def acceptable(date) -> bool:
    return date <= MAX_DATE


def start(notify: Notify):
    while True:
        req = requests.get(URL, cookies=COOKIES)
        soup = BeautifulSoup(req.content, "html.parser")

        date = extract_first_date(soup)
        print(date)

        if acceptable(date):
            notify.send(f'Appointment available at {date}')
            print('notification sent')

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
