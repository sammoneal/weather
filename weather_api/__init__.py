"""
Entrypoint for WeatherAPI to make requests of the National 
Weather Service API as well as access and process the response.

Also contains helper functions and reference data. 
"""
from .nws_api import NWS as WeatherAPI
from .nws_api import geolocator
