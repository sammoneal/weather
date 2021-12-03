import requests
from collections import namedtuple
from geopy.geocoders import Nominatim

api_url = "https://api.weather.gov/points/"

Cords = namedtuple('Cords', ['lat', 'lng'])

geolocator = Nominatim(user_agent='flask_weather')

class WeatherAPI():

    def __init__(self, cords) -> None:
        self.cords = cords
        url_endpoint = api_url + f"{self.cords.lat},{self.cords.lng}"
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

    dc_weather = WeatherAPI(dc)
    kirk_weather = WeatherAPI(kirkland)

    my_location = geolocator.geocode(input('Enter a US location:'))
    my_weather = WeatherAPI(Cords(my_location.latitude,my_location.longitude))

    for obj in [dc_weather,kirk_weather,my_weather]:
        print(f"*****{obj.city}*****")
        for item in obj.forecast:
            print(f"{item['name']}: {item['shortForecast']} {item['temperature']}F")
        print('\n')
