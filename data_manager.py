import requests
import os
from dotenv import load_dotenv
SHEETY_LINK = os.getenv("SHEETY_LINK")
AUTH = os.getenv("AUTH")

SHEETY_HEADERS = {
    "Authorization": AUTH
}

TEQ_APIKEY = os.getenv("TEQ_APIKEY")
TEQ_LINK_QUERY = os.getenv("TEQ_LINK_QUERY")
city_list = []
cities = requests.get(url=SHEETY_LINK, headers=SHEETY_HEADERS)
cities = cities.json()
cities = cities['prices']
teq_headers = {
    "apikey": TEQ_APIKEY
}
teq_params = {
    "term": "",
    "name": ""
}


class DataManager:

    def getIATA(self):
        cities = requests.get(url=SHEETY_LINK, headers=SHEETY_HEADERS)
        cities = cities.json()
        cities = cities['prices']
        for city in cities:
            city_list.append(city['iataCode'])
        return city_list
    def addIATA(self):
        cities = requests.get(url=SHEETY_LINK, headers=SHEETY_HEADERS)
        cities = cities.json()
        cities = cities['prices']
        counter = 2
        sheety_json = {
            "price": {
                "iataCode": ""
            }
        }
        for city in cities:
            iata = requests.get(
                url=f"https://api.tequila.kiwi.com/locations/query?term={city['city']}&"
                    f"=limit=10&active_only=true",
                headers=teq_headers)
            iata.raise_for_status()
            iata = iata.json()
            iata = iata['locations'][0]['code']
            sheety_json['price']['iataCode'] = iata
            Sheety_PUT = os.getenv("SHEETY_PUT")
            put_IATA = requests.put(url=Sheety_PUT, json=sheety_json, headers=SHEETY_HEADERS)
            put_IATA.raise_for_status()
            counter += 1



