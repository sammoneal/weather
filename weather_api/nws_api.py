import re
from collections import namedtuple
from itertools import chain
from datetime import datetime
from geopy.geocoders import Nominatim
import requests
from .icon_maps import conditions_map

Cords = namedtuple("Cords", ["lat", "long"])

geolocator = Nominatim(user_agent="flask_weather")


class NWS:
    BASE_URL = "https://api.weather.gov/points/"

    def __init__(self, lat, long) -> None:
        self.lat, self.long = lat, long

        self.url = self.BASE_URL + f"{self.lat},{self.long}"
        self.geo = requests.get(self.url).json()

        self.location = self.geo["properties"]["relativeLocation"]
        self.url_forecast = self.geo["properties"]["forecast"]
        self.url_hourly = self.geo["properties"]["forecastHourly"]

        self.forecast = self.get_forecast(self.url_forecast)
        self.hourly = self.get_forecast(self.url_hourly)

        self.current = self.forecast[0]

        for item in chain(self.forecast, self.hourly):
            # Time code
            item["time"] = datetime.strptime(
                item["startTime"][:19], "%Y-%m-%dT%H:%M:%S"
            )
            # Icon map
            conditions = re.split("then", item["shortForecast"])
            try:
                icon_set = conditions_map[conditions[0]]
                if item["isDaytime"]:
                    item["icon"] = icon_set[0]
                else:
                    item["icon"] = icon_set[-1]
            except LookupError:
                item["icon"] = "wi-alien"
            # Percipitation fix
            precip = item["probabilityOfPrecipitation"]["value"]
            precip = precip if precip else 0
            # Wind icon
            item["windIcon"] = f"wi wi-wind towards-{item['windDirection'].lower()}"

    @property
    def city(self):
        loc = self.location["properties"]
        return f"{loc['city']}, {loc['state']}"

    @staticmethod
    def get_forecast(url):
        weather = requests.get(url).json()
        return weather["properties"]["periods"]
