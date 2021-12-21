import requests
from collections import namedtuple
from geopy.geocoders import Nominatim

Cords = namedtuple('Cords', ['lat', 'lng'])

geolocator = Nominatim(user_agent='flask_weather')

class WeatherAPI():

    API_URL = "https://api.weather.gov/points/"

    def __init__(self, lat, lng) -> None:
        self.lat, self.lng = lat, lng
        url_endpoint = self.API_URL + f"{self.lat},{self.lng}"
        geo = requests.get(url_endpoint).json()
        self.location = geo["properties"]['relativeLocation']
        self.url_forecast = geo["properties"]['forecast']
        self.url_hourly = geo["properties"]['forecastHourly']
        self.forecast = self.get_forecast(self.url_forecast)
        self.hourly = self.get_forecast(self.url_hourly)

    @property
    def city(self):
        loc = self.location['properties']
        return f"{loc['city']}, {loc['state']}"

    @staticmethod
    def get_forecast(url):
        weather = requests.get(url).json()
        return weather['properties']['periods']


if __name__ == '__main__':
    dc = Cords(38.8894,-77.0352)
    kirkland = Cords(47.6769,-122.2060)

    dc_weather = WeatherAPI(*dc)
    print(dc_weather.city)
    kirk_weather = WeatherAPI(*kirkland)

    my_location = geolocator.geocode(input('Enter a US location:'))
    my_weather = WeatherAPI(my_location.latitude,my_location.longitude)

    for obj in [dc_weather,kirk_weather,my_weather]:
        print(f"*****{obj.city}*****")
        for item in obj.forecast:
            print(f"{item['name']}: {item['shortForecast']} {item['temperature']}F")
        print('\n')

    print(f"*****{my_weather.city}*****")
    for index, item in enumerate(my_weather.hourly):
        print(f"Now+{index}: {item['shortForecast']} {item['temperature']}F")
        if index > 8:
            break

