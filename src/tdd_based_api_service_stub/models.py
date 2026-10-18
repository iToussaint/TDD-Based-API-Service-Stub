"""Data models for weather requests and responses."""

from dataclasses import dataclass

from tdd_based_api_service_stub.exceptions import InvalidRequestError


@dataclass(frozen=True, slots=True)
class ForecastRequest:
    """A validated request for a city's forecast.

    The city name is normalised on creation: surrounding and repeated
    whitespace is removed and the name is title-cased, so ``"  new   york "``
    becomes ``"New York"``.

    Attributes:
        city: The normalised city name.

    Raises:
        InvalidRequestError: If ``city`` is not a string or is blank.
    """

    city: str

    def __post_init__(self) -> None:
        """Validate and normalise the city name."""
        if not isinstance(self.city, str):
            raise InvalidRequestError(
                f"City must be a string, got {type(self.city).__name__}."
            )
        normalised = " ".join(self.city.split()).title()
        if not normalised:
            raise InvalidRequestError("City must not be empty.")
        object.__setattr__(self, "city", normalised)


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
