import re, math
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
        self.metadata = requests.get(self.url).json()
        self.forecast = self.get_forecast(self.metadata["properties"]["forecast"])
        self.hourly = self.get_forecast(self.metadata["properties"]["forecastHourly"])

        self.max_temp = self.current["temperature"]
        self.min_temp = self.max_temp
        self.max_wind = 20

        # Process the response
        for item in chain(self.forecast, self.hourly):
            # Time code
            item["time"] = datetime.strptime(
                item["startTime"][:19], "%Y-%m-%dT%H:%M:%S"
            )
            # Icon map
            conditions = re.split("then", item["shortForecast"])
            try:
                icon_set = conditions_map[conditions[0].strip()]
                if item["isDaytime"]:
                    item["icon"] = icon_set[0]
                else:
                    item["icon"] = icon_set[-1]
            except LookupError:
                item["icon"] = "wi-alien"
            # Percipitation value fix
            precip = item["probabilityOfPrecipitation"]["value"]
            if not precip:
                item["probabilityOfPrecipitation"]["value"] = 0
            # Wind value(s) fix
            wind_vals = re.findall('\d+',item["windSpeed"])
            item["windSpeed"] = max((int(val) for val in wind_vals))
            # Wind icon
            item["windIcon"] = f"wi-towards-{item['windDirection'].lower()}"
            if item["temperature"] > self.max_temp:
                self.max_temp = item["temperature"]
            elif item["temperature"] < self.min_temp:
                self.min_temp = item["temperature"]

        # Round min and max for cleaner charts
        step = 5
        self.min_temp = math.floor(self.min_temp / step) * step
        self.max_temp = math.ceil(self.max_temp / step) * step
        self.max_wind = math.ceil(self.max_wind / step) * step
        self.temp_spread = self.max_temp - self.min_temp
        self.temp_labels = []
        for i in range(1, 4):
            self.temp_labels.append(round(i * 0.25 * self.temp_spread) + self.min_temp)
        self.temp_labels.insert(0, self.min_temp)
        self.temp_labels.append(self.max_temp)
        self.temp_labels.reverse()

    @property
    def city(self):
        location = self.metadata["properties"]["relativeLocation"]["properties"]
        return f"{location['city']}, {location['state']}"

    @property
    def current(self):
        return self.forecast[0]

    @staticmethod
    def get_forecast(url):
        weather = requests.get(url).json()
        return weather["properties"]["periods"]
    
    def round_statistics(self, step = 5):
        self.min_temp = math.floor(self.min_temp / step) * step
        self.max_temp = math.ceil(self.max_temp / step) * step
        self.max_wind = math.ceil(self.max_wind / step) * step

