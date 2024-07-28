"""Simple response miner
"""

import time
from .nws_api import NWS as WeatherAPI, geolocator

CITIES = [
    "Boston",
    "Orlando",
    "Tucson",
    "San Diego",
    "Casper",
    "Chyenne",
    "Honolulu",
    "Albany",
    "Chicago",
    "Fargo",
    "Seattle",
    "Houston",
    "Topeka",
    "Allentown",
    "St. Louis",
    "Boise",
    "Portland",
    "Mesa AZ",
    "Las Vegas",
    "Lexington",
    "Denver",
    "Tampa",
    "Philadelphia",
    "Detroit",
]

CONDITIONS = set()

for city in CITIES:
    try:
        geo = geolocator.geocode(city, country_codes="US")
        weather = WeatherAPI(geo.latitude, geo.longitude)
        for item in weather.forecast:
            condition = item["shortForecast"]
            CONDITIONS.add(condition)
        time.sleep(5)
    except KeyError:
        continue

with open("test.txt", "w") as file:
    sorted_cond = list(CONDITIONS)
    sorted_cond.sort()
    for condition in sorted_cond:
        file.write(f"{condition}\n")
