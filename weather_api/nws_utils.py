import re
from .icon_maps import conditions_map

def numeric_wind(wind_string:str)->int:
    wind_vals = re.findall("\d+", wind_string)
    return max((int(val) for val in wind_vals))

def numeric_precip(precip)->int:
    if precip:
        return precip
    return 0

def icon_mapper(record:dict)->str:
    conditions = re.split("then", record["shortForecast"])
    try:
        icon_set = conditions_map[conditions[0].strip()]
        if record["isDaytime"]:
            return icon_set[0]
        return icon_set[-1]
    except LookupError:
        return "wi-alien"