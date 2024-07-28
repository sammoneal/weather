"""
Contains the WeatherStat and WeatherStatManager classes.
These classes are used by NWS to find the stats used to draw charts.
"""

import math
from typing import Callable
from .nws_utils import numeric_wind, numeric_precip


class WeatherStatManager:
    """Manages the stats that are graphed: temperature, percipiation, and wind speed."""

    def __init__(self, init_cond: dict) -> None:
        self.temp = WeatherStat(init_cond["temperature"])
        self.precip = WeatherStat(
            numeric_precip(init_cond["probabilityOfPrecipitation"]["value"])
        )
        self.wind = WeatherStat(numeric_wind(init_cond["windSpeed"]))

    def record_temp(self, value: int) -> None:
        """Feed temperature into the stat manager.

        Args:
            value (int): value to be compared.
        """
        self.temp.record(value)

    def record_wind(self, value: int) -> None:
        """Feed temperature into the stat manager.

        Args:
            value (int): value to be compared.
        """
        self.wind.record(value)

    def record_precip(self, value: int) -> None:
        """Feed temperature into the stat manager.

        Args:
            value (int): value to be compared.
        """
        self.precip.record(value)

    def analyze(self) -> None:
        """Steps and makes ranges for all stats."""
        for item in self:
            item.make_range()

    def __iter__(self):
        return (stat for stat in [self.temp, self.precip, self.wind])


class WeatherStat:
    """
    Keeps track of min and max as numbers are fed into the object via record(). 
    Rounds bounds to neat intervals and generates evenly spaced intermediate values.
    """
    STEP = 5

    def __init__(self, initial_value) -> None:
        self._max = initial_value
        self._min = initial_value
        self.values = None

    @property
    def max(self) -> int:
        """Returns the highest value.

        Returns:
            int: Maximum value
        """
        return self._max

    @property
    def min(self) -> int:
        """Returns the smallest value

        Returns:
            int: Minimum value
        """
        return self._min

    @property
    def diff(self) -> int:
        """Spread between minimum and maximum

        Returns:
            int: Max/Min difference
        """
        return self.max - self.min

    def record(self, value: int) -> None:
        """Records value if it is a new minimum or maximum.

        Args:
            value (int): Value to be recorded.
        """
        if value > self.max:
            self._max = value
        elif value < self.min:
            self._min = value

    def make_range(self) -> None:
        """Generates a range of five evenly spaced values starting with max and ending with min.
        """
        self.step_stats()
        generated = []
        for i in range(1, 4):
            generated.append(round(i * 0.25 * self.diff) + self.min)
        #Descending order for template constructor loop
        generated.reverse()
        self.values = [self.max] + generated + [self.min]

    def step_stats(self) -> None:
        """Steps min down and max up.
        """
        self._min = self.step(self.min, math.floor)
        self._max = self.step(self.max, math.ceil)

    def step(self, value:int, func:Callable)->int:
        """Steps by the class global STEP given a value and rounding function.

        Args:
            value (int): Walue to be stepped
            func (Callable): Stepping function

        Returns:
            int: Stepped value
        """
        return func(value / self.STEP) * self.STEP

    def __iter__(self):
        if not self.values:
            self.make_range()
        return (value for value in self.values)
