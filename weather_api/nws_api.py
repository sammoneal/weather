from itertools import chain
from datetime import datetime
from geopy.geocoders import Nominatim
import requests
from .stat_manager import WeatherStatManager
from .nws_utils import icon_mapper, numeric_wind, numeric_precip

geolocator = Nominatim(user_agent="flask_weather")


class NWS:
    BASE_URL = "https://api.weather.gov/points/"

    def __init__(self, latitude, longitude) -> None:
        self.metadata = requests.get(
            self.BASE_URL + f"{latitude},{longitude}", timeout=10
        ).json()
        self.forecast = self.get_forecast(self.metadata["properties"]["forecast"])
        self.hourly = self.get_forecast(self.metadata["properties"]["forecastHourly"])

        # Use stat manager for min, max, range, spread, & labels
        self.stats = WeatherStatManager(self.current)

        # Process the response
        self.clean_forecast_data()
        self.stats.analyze()

    @property
    def city(self):
        location = self.metadata["properties"]["relativeLocation"]["properties"]
        return f"{location['city']}, {location['state']}"

    @property
    def coords(self):
        return self.metadata["properties"]["relativeLocation"]["geometry"][
            "coordinates"
        ]

    @property
    def current(self):
        return self.forecast[0]

    @staticmethod
    def get_forecast(url):
        weather = requests.get(url).json()
        return weather["properties"]["periods"]

    def clean_forecast_data(self):
        for item in chain(self.forecast, self.hourly):
            # Time code
            item["time"] = datetime.strptime(
                item["startTime"][:19], "%Y-%m-%dT%H:%M:%S"
            )
            # Fix Values
            item["windSpeed"] = numeric_wind(item["windSpeed"])
            item["probabilityOfPrecipitation"]["value"] = numeric_precip(item["probabilityOfPrecipitation"]["value"])
            # Stats
            self.stats.record_temp(item["temperature"])
            self.stats.record_precip(item["probabilityOfPrecipitation"]["value"])
            self.stats.record_wind(item["windSpeed"])
            # Icons
            item["icon"] = icon_mapper(item)
            item["windIcon"] = f"wi-towards-{item['windDirection'].lower()}"
