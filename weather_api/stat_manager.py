import math
from .nws_utils import numeric_wind, numeric_precip

class WeatherStatManager():
    def __init__(self, init_cond) -> None:
        self.temp = WeatherStat(init_cond['temperature'])
        self.precip = WeatherStat(numeric_precip(init_cond["probabilityOfPrecipitation"]["value"]))
        self.wind = WeatherStat(numeric_wind(init_cond['windSpeed']))
    
    def record_temp(self, value):
        self.temp.record_stat(value)

    def record_wind(self, value):
        self.wind.record_stat(value)

    def record_precip(self, value):
        self.precip.record_stat(value)

    def analyze(self):
        for item in self:
            item.make_range()

    def __iter__(self):
        return (stat for stat in [self.temp, self.precip, self.wind])

class WeatherStat():
    STEP = 5

    def __init__(self, initial_value=0) -> None:
        self.values = [initial_value, initial_value]

    @property
    def max(self):
        return self.values[0]

    @property
    def min(self):
        return self.values[-1]
    
    @property
    def diff(self):
        return self.max - self.min

    def record_stat(self, value):
        if value > self.max:
            self.values[0] = value
        elif value < self.min:
            self.values[-1] = value
    
    def make_range(self):
        self.step_stats()
        generated = []
        for i in range(1, 4):
            generated.append(round(i * 0.25 * self.diff) + self.min)
        generated.reverse()
        self.values = [self.max] + generated + [self.min]

    def step_stats(self):
        self.values[-1] = math.floor(self.min / self.STEP) * self.STEP
        self.values[0] = math.ceil(self.max / self.STEP) * self.STEP
