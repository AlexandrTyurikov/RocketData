import requests
import json
import sys
import time
import threading

"""class Spinner - визуализация ожидания"""


class Spinner:
    busy = False
    delay = 0.4

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)


headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
    'accept': '*/*'
}
url_cities = "https://apigate.tui.ru/api/office/cities"
date = []
phones = []


def tui_pars():
    request_cities = requests.get(url_cities, headers=headers)
    if request_cities.status_code == 200:
        print("Идет процесс парсинга")
        spinner = Spinner()
        spinner.start()
        for id_city in request_cities.json()['cities']:
            url_office = f"https://apigate.tui.ru/api/office/list?cityId={id_city['cityId']}&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false"
            request_offices = requests.get(url_office, headers=headers)
            for office in request_offices.json()['offices']:
                phones.clear()
                for i in office['phones']:
                    phones.append(i['phone'])
                    phones.append(i['url'][4:])
                if office['hoursOfOperation']['saturday']['isDayOff'] == False:
                    saturday = f"{office['hoursOfOperation']['saturday']['startStr']} до {office['hoursOfOperation']['saturday']['endStr']}"
                else:
                    saturday = "выходной"
                if office['hoursOfOperation']['sunday']['isDayOff'] == False:
                    sunday = f"{office['hoursOfOperation']['sunday']['startStr']} до {office['hoursOfOperation']['sunday']['endStr']}"
                else:
                    sunday = "выходной"
                date.append({
                    'address': office['address'],
                    'latlon': [float(office['latitude']), float(office['longitude'])],
                    'name': office['name'],
                    'phones': phones,
                    'working_hours': [
                        f"будние дни {office['hoursOfOperation']['workdays']['startStr']} до {office['hoursOfOperation']['workdays']['endStr']}",
                        f"суббота {saturday}",
                        f"воскресенье {sunday}"
                    ]
                })
        spinner.stop()
        print("Процесс окончен")
    with open('data_site_2.json', 'w', encoding='utf-8') as file:
        json.dump(date, file, indent=4, ensure_ascii=False)


tui_pars()
