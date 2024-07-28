"""
Helper functions for processing NWS responses.
"""

import re
from .icon_maps import conditions_map


def numeric_wind(wind_string: str) -> int:
    """Removes units and whitespace from the speed value.
    If multiple values are present in the string, returns the largest.

    Args:
        wind_string (str): String to be searched.

    Returns:
        int: Highest windspeed.
    """
    wind_vals = re.findall(r"\d+", wind_string)
    return max((int(val) for val in wind_vals))


def numeric_precip(precip) -> int:
    """Replaces None type values with zero.

    Args:
        precip (_type_): Initial value.

    Returns:
        int: Integer value.
    """
    if precip:
        return precip
    return 0


def icon_mapper(record: dict) -> str:
    """Assigns an icon based on the short forecast and time of day.

    Args:
        record (dict): Weather forecast data point.

    Returns:
        str: Icon as CSS class.
    """
    conditions = re.split("then", record["shortForecast"])
    try:
        icon_set = conditions_map[conditions[0].strip()]
        if record["isDaytime"]:
            return icon_set[0]
        return icon_set[-1]
    except LookupError:
        return "wi-alien"


def theme_mapper(conditions: str) -> str:
    """Assigns a stylesheet based on the current conditions.

    Args:
        conditions (str): Current conditions description as string.

    Returns:
        str: Stylesheet name without .css file extension.
    """
    conditions = conditions.lower()
    trigger_conditions = ['storm','snow','rain']
    for item in trigger_conditions:
        if conditions.find(item) > 0:
            return item
    if max(conditions.find('haze'), conditions.find('fog')) > 0:
        return 'fog'
    elif conditions == 'sunny':
        return 'sunny'
    elif conditions in ['cloudy', 'mostly cloudy']:
        return 'cloudy'
    return 'clear'