"""Data models for weather requests and responses."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Forecast:
    """A weather forecast for a single city.

    Attributes:
        city: The city the forecast is for.
        temperature_celsius: The temperature in degrees Celsius.
        condition: A short description such as ``"Sunny"``.
        humidity_percent: The relative humidity, from 0 to 100.
        wind_speed_kph: The wind speed in kilometres per hour.
    """

    city: str
    temperature_celsius: float
    condition: str
    humidity_percent: int
    wind_speed_kph: float
