import sys
from textwrap import fill

from weather_api import WeatherAPI, geolocator

location = geolocator.geocode(sys.argv[1], country_codes="US")

weather = WeatherAPI(location.latitude, location.longitude)
for item in weather.forecast:
    if item["number"] == 1:
        current = item

print(
    f'{"  "+weather.city+"  ":*^75}\n\n{current["name"]}: {fill(current["detailedForecast"],65)}\n'
)

for item, _ in zip(weather.hourly, range(24)):
    time = item["time"]
    short = item["shortForecast"]
    temp = item["temperature"]
    precip = item["probabilityOfPrecipitation"]["value"]
    day = "Day" if item["isDaytime"] else "Night"

    wind = item["windSpeed"]
    wind_dir = item["windDirection"]

    output = f'{time.month:<2}/{time.day:<2}  {time.hour%12:>2}:00{"AM" if time.hour < 12 else "PM"}  {day:<5}  {short:<30}  {temp:>3}F  {precip:>3}%  {wind:>6} {wind_dir:<3}'
    print(output)
