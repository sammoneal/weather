import requests
from collections import namedtuple
from geopy.geocoders import Nominatim

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

    @property
    def city(self):
        loc = self.location["properties"]
        return f"{loc['city']}, {loc['state']}"

    @staticmethod
    def get_forecast(url):
        weather = requests.get(url).json()
        return weather["properties"]["periods"]
