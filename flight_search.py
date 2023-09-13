import requests
import os
from dotenv import load_dotenv
from flight_data import FlightData

TEQ_APIKEY = os.getenv("TEQ_APIKEY")

TEQ_HEADERS = {
    "apikey": TEQ_APIKEY
}
SHEETY_LINK = os.getenv("SHEETY_LINK")
AUTH = os.getenv("AUTH")

SHEETY_HEADERS = {
    "Authorization": AUTH
}


class FlightSearch:
    def __init__(self, begin, end, flyto):
        self.searchdata = {}
        self.begindate = begin
        self.enddate = end
        self.flyfrom = "NYC"
        self.flyto = flyto

    def flightSearch(self):
        counter = 0
        cities = requests.get(url=SHEETY_LINK, headers=SHEETY_HEADERS)
        cities = cities.json()
        cities = cities['prices']

        for city in self.flyto:
            cur_city = cities[counter]
            print(f"City {cur_city}")
            counter += 1
            cur_price = cur_city["lowestPrice"]
            print(f"Cur price: {cur_price}\n")
            cur_id = int(cur_city["id"])

            search_params = {
                "fly_from": self.flyfrom,
                "fly_to": city,
                "date_from": self.begindate,
                "date_to": self.enddate,
                "max_stopovers": 0
            }

            searchdeals = requests.get(url="https://api.tequila.kiwi.com/v2/search", headers=TEQ_HEADERS,
                                       params=search_params)
            searchdeals.raise_for_status()
            searchdeals = searchdeals.json()
            searchdeals = searchdeals['data']
            if not searchdeals:
                continue
            try:
                price = f"{searchdeals[0]['price']}"
            except IndexError:
                print("No flights found.")
            else:
                print(price)
                if int(price) < int(cur_price):
                    print("Deal found!")
                    sheety_json = {
                        "price": {
                            "lowestPrice": price,
                        }
                    }
                    Sheety_PUT = os.getenv("SHEETY_PUT2")
                    put_price = requests.put(url=Sheety_PUT, json=sheety_json, headers=SHEETY_HEADERS)
                    put_price.raise_for_status()
                    from_airport = searchdeals[0]['flyFrom']
                    to_airport = searchdeals[0]["flyTo"]
                    from_city = searchdeals[0]["cityFrom"]
                    to_city = searchdeals[0]["cityTo"]

                    depart = searchdeals[0]["local_departure"]
                    arrive = searchdeals[0]["local_arrival"]
                    data = FlightData(fromair=from_airport, toair=to_airport, fromcity=from_city, tocity=to_city,
                                      depart=depart, arrive=arrive, price=price)
                    return data
    # This class is responsible for talking to the Flight Search API.
