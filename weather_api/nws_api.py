"""
Contains the NWS class for requesting data from the National Weather Service API 
and shaping it for the weather route templates.
"""

import re
from itertools import chain
from datetime import datetime
from geopy.geocoders import Nominatim
import requests
from .stat_manager import WeatherStatManager
from .nws_utils import icon_mapper, numeric_wind, numeric_precip, theme_mapper

geolocator = Nominatim(user_agent="flask_weather")


class NWS:
    """
    Makes requests to the National Weather Service API and
    """

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
        self.theme = theme_mapper(re.split("then", self.forecast[0]["shortForecast"])[0])
        self.stats.analyze()

    @property
    def city(self) -> str:
        """City and State of the weather forecast.

        Returns:
            str: City and state abbreviation seperated by a comma.
        """
        location = self.metadata["properties"]["relativeLocation"]["properties"]
        return f"{location['city']}, {location['state']}"

    @property
    def coords(self) -> list:
        """Geographic coordinates of the weather forecast.

        Returns:
            list: Two items, latitude and longitude
        """
        return self.metadata["properties"]["relativeLocation"]["geometry"][
            "coordinates"
        ]

    @property
    def current(self) -> dict:
        """Current conditions.

        Returns:
            dict: First entry in the forecast.
        """
        return self.forecast[0]

    @staticmethod
    def get_forecast(url) -> dict:
        """Pings an API endpoint and trims metadata

        Args:
            url (_type_): URL to be requested

        Returns:
            dict: JSON response trimmed and converted to dict
        """
        weather = requests.get(url, timeout=10).json()
        return weather["properties"]["periods"]

    def clean_forecast_data(self):
        """
        Processes the forecast and hourly responses.
        Includes stat collection and icon assignment.
        """
        for item in chain(self.forecast, self.hourly):
            # Time code
            item["time"] = datetime.strptime(
                item["startTime"][:19], "%Y-%m-%dT%H:%M:%S"
            )
            # Fix Values
            item["windSpeed"] = numeric_wind(item["windSpeed"])
            item["probabilityOfPrecipitation"]["value"] = numeric_precip(
                item["probabilityOfPrecipitation"]["value"]
            )
            # Stats
            self.stats.record_temp(item["temperature"])
            self.stats.record_precip(item["probabilityOfPrecipitation"]["value"])
            self.stats.record_wind(item["windSpeed"])
            # Icons
            item["icon"] = icon_mapper(item)
            item["windIcon"] = f"wi-towards-{item['windDirection'].lower()}"
